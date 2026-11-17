/* Userspace HFSX importer; link against planetbeing/libdmg-hfsplus.
 * Input: NUL-delimited groups of type, destination, source/target, octal mode,
 * decimal uid, decimal gid. No device access. Files stream through libhfs.
 * Hard links are materialized as copies; compression xattrs aren't copied.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <hfs/hfsplus.h>
#include <hfs/hfslib.h>
#include "abstractfile.h"

char endianness;
static const char *current_path, *current_source;
static void report_pending(void)
{
    if (current_path) fprintf(stderr, "unfinished: %s source: %s\n", current_path, current_source);
}
static void die(const char *path) { fprintf(stderr, "import failed: %s\n", path); exit(1); }
struct mapped_image { unsigned char *bytes; size_t size; int fd; };
static int mapped_read(io_func *io, off_t off, size_t n, void *out)
{
    struct mapped_image *m = io->data;
    if (off < 0 || (uint64_t)off > m->size || n > m->size - off) {
        fprintf(stderr, "image read outside bounds: %lld + %zu\n", (long long)off, n);
        return FALSE;
    }
    memcpy(out, m->bytes + off, n);
    return TRUE;
}
static int mapped_write(io_func *io, off_t off, size_t n, void *in)
{
    struct mapped_image *m = io->data;
    if (off < 0 || (uint64_t)off > m->size || n > m->size - off) {
        fprintf(stderr, "image write outside bounds: %lld + %zu\n", (long long)off, n);
        return FALSE;
    }
    memcpy(m->bytes + off, in, n);
    return TRUE;
}
static void mapped_close(io_func *io)
{
    struct mapped_image *m = io->data;
    if (msync(m->bytes, m->size, MS_SYNC) || fsync(m->fd)) die("flush image");
    munmap(m->bytes, m->size);
    close(m->fd);
    free(m);
    free(io);
}
static io_func *mapped_open(const char *path)
{
    struct stat st;
    struct mapped_image *m = calloc(1, sizeof(*m));
    io_func *io = calloc(1, sizeof(*io));
    m->fd = open(path, O_RDWR);
    if (m->fd < 0 || fstat(m->fd, &st) || !S_ISREG(st.st_mode)) die(path);
    m->size = st.st_size;
    m->bytes = mmap(NULL, m->size, PROT_READ | PROT_WRITE, MAP_SHARED, m->fd, 0);
    if (m->bytes == MAP_FAILED) die(path);
    io->data = m;
    io->read = mapped_read;
    io->write = mapped_write;
    io->close = mapped_close;
    return io;
}
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    atexit(report_pending);
    uint16_t endian_test = 1;
    endianness = *(uint8_t *)&endian_test ? IS_LITTLE_ENDIAN : IS_BIG_ENDIAN;
    io_func *io = mapped_open(argv[1]);
    if (!io) die(argv[1]);
    Volume *v = openVolume(io);
    if (!v) die(argv[1]);
    unsigned count = 0;
    for (;;) {
        char *a[6] = {0};
        for (int i = 0; i < 6; ++i) {
            size_t n = 0;
            ssize_t len = getdelim(&a[i], &n, 0, stdin);
            if (len < 0) {
                if (i || !feof(stdin)) die("truncated input");
                free(a[i]);
                goto done;
            }
            if (!len || a[i][len-1]) die("unterminated input");
        }
        current_path = a[1];
        current_source = a[2];
        HFSPlusCatalogRecord *r = getRecordFromPath3(a[1], v, NULL, NULL, TRUE, FALSE, kHFSRootFolderID);
        if (a[0][0] == 'd') {
            if (!r && !newFolder(a[1], v)) die(a[1]);
            if (r && r->recordType != kHFSPlusFolderRecord) die(a[1]);
        } else {
            if (r) die(a[1]); /* Never overwrite through an existing link. */
            if (a[0][0] == 'l') {
                if (!makeSymlink(a[1], a[2], v)) die(a[1]);
            } else if (a[0][0] == 'f') {
                FILE *f = fopen(a[2], "rb");
                if (!f) die(a[2]);
                if (!add_hfs(v, createAbstractFileFromFile(f), a[1])) die(a[1]);
            } else die("unknown entry type");
        }
        free(r);
        r = getRecordFromPath3(a[1], v, NULL, NULL, TRUE, FALSE, kHFSRootFolderID);
        if (!r) die(a[1]);
        HFSPlusBSDInfo *p;
        if (r->recordType == kHFSPlusFolderRecord) p = &((HFSPlusCatalogFolder *)r)->permissions;
        else if (r->recordType == kHFSPlusFileRecord) p = &((HFSPlusCatalogFile *)r)->permissions;
        else { die(a[1]); return 1; }
        p->fileMode = strtoul(a[3], NULL, 8);
        p->ownerID = strtoul(a[4], NULL, 10);
        p->groupID = strtoul(a[5], NULL, 10);
        if (!updateCatalog(v, r)) die(a[1]);
        free(r);
        if (!(++count % 1000)) fprintf(stderr, "imported %u: %s\n", count, a[1]);
        current_path = current_source = NULL;
        for (int i = 0; i < 6; ++i) free(a[i]);
    }
done:
    closeVolume(v);
    CLOSE(io);
    fprintf(stderr, "import complete: %u entries\n", count);
    return 0;
}

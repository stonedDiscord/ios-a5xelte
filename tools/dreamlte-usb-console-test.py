#!/usr/bin/env python3
"""Exercise actual bounded S8 console readers and source-backed bus setup."""
import pathlib
import re
import subprocess
import sys
import tempfile

def function(source, name):
    match = re.search(r'\b' + name + r'\([^;{}]*\)\s*\{', source)
    assert match, name
    opening = source.index('{', match.start())
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    code = source[match.start():end]
    return re.sub(r'__asm__ volatile\("[^"\n]*" ::: "memory"\);', '', code)

root = pathlib.Path(sys.argv[1])
early = (root/'osfmk/arm64/sweet_early.c').read_text()
usb = (root/'bsd/dev/sweet_usb.c').read_text()
code = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define DREAMLTE_LOG_BASE_PA 0x91a00000u
#define DREAMLTE_LOG_END_PA 0x91c00000u
static uint32_t cursor;
static unsigned char buffer[0x200000];
static volatile uint32_t *dreamlte_log_cursor = &cursor;
static volatile uint8_t *dreamlte_log_base = buffer;
typedef uintptr_t vm_offset_t;
static uint32_t regs[0x10000/4];
static uint32_t usb_rd(vm_offset_t base, unsigned off) {
    return *(uint32_t *)(base + off);
}
'''
code += 'uint64_t\n' + function(early, 'dreamlte_console_position') + '\n'
code += 'uint32_t\n' + function(early, 'dreamlte_console_copy') + '\n'
code += 'static int\n' + function(usb, 'dreamlte_usb_console_read') + '\n'
code += 'static void\n' + function(usb, 'dreamlte_usb_core_timing') + '\n'
code += r'''
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/uio.h>
#include <setjmp.h>
#define __unused __attribute__((unused))
typedef int wait_result_t;
typedef void *socket_t;
static struct { int configured; } ud = {1};
static jmp_buf finished;
static unsigned sleeps, sends, send_mode;
static uint32_t sent_lengths[4];
static unsigned char sent_bytes[4096];
static unsigned sent_count;
static void bzero(void *p, size_t n) { memset(p, 0, n); }
static void ud_sleep_ms(unsigned ms) {
    assert(ms == 100);
    if (++sleeps == 3) longjmp(finished, 1);
}
static int sock_socket(int domain, int type, int protocol, void *a, void *b, socket_t *so) {
    assert(domain == PF_INET && type == SOCK_DGRAM && protocol == IPPROTO_UDP && !a && !b);
    *so = (void *)1; return 0;
}
static int sock_send(socket_t so, struct msghdr *msg, int flags, size_t *sent) {
    assert(so && !flags && msg->msg_iovlen == 1 && sends < 4);
    struct sockaddr_in *to = msg->msg_name;
    assert(to->sin_addr.s_addr == htonl(0xc0a80701) && to->sin_port == htons(5140));
    struct iovec *v = msg->msg_iov;
    sent_lengths[sends++] = v->iov_len;
    if (sends == 1) { *sent = send_mode ? v->iov_len - 1 : 0; return send_mode ? 0 : -1; }
    assert(sent_count + v->iov_len <= sizeof(sent_bytes));
    memcpy(sent_bytes + sent_count, v->iov_base, v->iov_len);
    sent_count += v->iov_len; *sent = v->iov_len; return 0;
}
#define sweet_log_position dreamlte_console_position
#define sweet_log_copy dreamlte_console_copy
'''
sender = function(usb, 'ud_log_thread')
# Linux host sockaddr_in lacks Darwin's length byte; network fields stay real.
sender = sender.replace('to.sin_len = sizeof(to);', '')
code += 'static void\n' + sender + '\n'
code += r'''
int main(void) {
    char out[1402];
    for (unsigned i = 0; i < sizeof(buffer); i++) buffer[i] = i;
    uint64_t pos = 0;
    for (unsigned i = 0; i < 5; i++) {
        cursor = (uint32_t[]){0, DREAMLTE_LOG_BASE_PA-1,
            DREAMLTE_LOG_END_PA+1, 0xffffffff, DREAMLTE_LOG_BASE_PA}[i];
        assert(dreamlte_console_position() == 0);
        assert(dreamlte_console_copy(&pos, out, sizeof(out)) == 0 && pos == 0);
    }
    cursor = DREAMLTE_LOG_BASE_PA + 2049;
    memset(out, 0x55, sizeof(out));
    assert(dreamlte_console_copy(&pos, out, 1400) == 1400 && pos == 1400);
    assert(out[1400] == 0x55 && out[1401] == 0x55);
    assert(!memcmp(buffer, out, 1400));
    assert(dreamlte_console_copy(&pos, out, 1400) == 649 && pos == 2049);
    assert(!memcmp(buffer+1400, out, 649));
    assert(!dreamlte_console_copy(&pos, out, 1400));
    cursor += 10;
    assert(dreamlte_console_copy(&pos, out, 0) == 0 && pos == 2049);
    assert(dreamlte_console_copy(&pos, out, 1400) == 10 && pos == 2059);
    cursor = DREAMLTE_LOG_END_PA;
    assert(dreamlte_console_position() == sizeof(buffer));
    pos = sizeof(buffer)-1;
    assert(dreamlte_console_copy(&pos, out, 1400) == 1 && out[0] == (char)255);
    assert(!dreamlte_console_copy(&pos, out, 1400));
    pos = UINT64_MAX;
    assert(!dreamlte_console_copy(&pos, out, 1400) && pos == UINT64_MAX);
    unsigned char reply[514];
    memset(reply, 0x55, sizeof(reply));
    assert(dreamlte_usb_console_read(0x52, 0, 0x8895, 8, reply) == 8);
    assert(!memcmp(reply, "DLOG\0\0\40\0", 8));
    assert(reply[8] == 0x55);
    for (uint32_t offset = 0; offset < sizeof(buffer); offset += 511) {
        memset(reply, 0x55, sizeof(reply));
        uint32_t want = sizeof(buffer) - offset;
        if (want > 512) want = 512;
        assert(dreamlte_usb_console_read(0x53, offset & 65535, offset >> 16, 512, reply) == (int)want);
        assert(!memcmp(reply, buffer + offset, want) && reply[want] == 0x55);
    }
    assert(dreamlte_usb_console_read(0x53, 0, 32, 512, reply) == 0);
    for (unsigned length = 0; length < 1024; length++) {
        if (length != 8) assert(dreamlte_usb_console_read(0x52, 0, 0x8895, length, reply) == -1);
        if (!length || length > 512) assert(dreamlte_usb_console_read(0x53, 0, 0, length, reply) == -1);
    }
    assert(dreamlte_usb_console_read(0x52, 1, 0x8895, 8, reply) == -1);
    assert(dreamlte_usb_console_read(0x52, 0, 0, 8, reply) == -1);
    assert(dreamlte_usb_console_read(0x53, 1, 32, 512, reply) == -1);
    assert(dreamlte_usb_console_read(0x53, 65535, 65535, 512, reply) == -1);
    assert(dreamlte_usb_console_read(0x54, 0, 0, 8, reply) == -1);
    for (unsigned i = 0; i < 34; i++) {
        uint32_t bus = i == 32 ? 0x22220001u : i == 33 ? 0x22220009u : 1u << i;
        memset(regs, 0, sizeof(regs));
        regs[0xc100/4] = bus;
        dreamlte_usb_core_timing((uintptr_t)regs);
        assert(regs[0xc100/4] == (bus | 9u));
        for (unsigned n = 0; n < sizeof(regs)/sizeof(regs[0]); n++)
            if (n != 0xc100/4 && n != 0xc110/4 && n != 0xc200/4) assert(!regs[n]);
    }
    for (send_mode = 0; send_mode < 2; send_mode++) {
        sleeps = sends = sent_count = 0;
        cursor = DREAMLTE_LOG_BASE_PA + 2049;
        if (!setjmp(finished)) ud_log_thread(NULL, 0);
        assert(sends == 3 && sent_count == 2049);
        assert(sent_lengths[0] == 1400 && sent_lengths[1] == 1400 && sent_lengths[2] == 649);
        assert(!memcmp(sent_bytes, buffer, 2049));
    }
    puts("PASS: actual bounded RAM console readers: invalid/empty/full cursors, chunking, append, zero max, saturated tail; INCR/INCR16 only, AXI/cache fields preserved; real sender retries failed/short sends without dropping chunks");
}
'''
assert '#define sweet_log_copy dreamlte_console_copy' in usb
assert '#define sweet_log_position dreamlte_console_position' in usb
assert 'sweet_ufs_init' not in usb
# DREAMLTE and donor both reach the sender; its body must not print.
sender = function(usb, 'ud_log_thread')
assert 'printf(' not in sender
with tempfile.TemporaryDirectory(prefix='dreamlte-console-') as tmp:
    path = pathlib.Path(tmp)
    (path/'test.c').write_text(code)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror',
                    str(path/'test.c'), '-o', str(path/'test')], check=True)
    result = subprocess.run([str(path/'test')], check=True, capture_output=True, text=True)
    print(result.stdout.splitlines()[-1])

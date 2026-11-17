/* A03 Jadard coordinate-report decoder; no bus, MMIO or firmware operations.
 * Layout: Samsung HS03 jdchipset/jadard_common.{c,h}, coordinate IRQ path.
 * This is preparation for a driver, not an enabled XNU touch provider.
 */
#ifndef A03_JD9365T_REPORT_H
#define A03_JD9365T_REPORT_H

#include <stddef.h>
#include <stdint.h>

#define A03_JD9365T_REPORT_SIZE 60u
#define A03_JD9365T_CONTACTS 10u

struct a03_jd9365t_contact {
	uint16_t x, y;
	uint8_t width, down;
};

struct a03_jd9365t_report {
	uint8_t reported_count;
	struct a03_jd9365t_contact contacts[A03_JD9365T_CONTACTS];
	uint8_t state[5];
};

/* Call only after a successful complete coordinate-report transfer from a
 * running, identified controller. Gesture/debug packets are different paths.
 * No checksum or freshness field is established by the coordinate parser.
 * A zero-filled transfer MUST NOT stand in for a failed bus read: zero is a
 * valid coordinate. positive reported_count is metadata, not a packed-contact bound;
 * the stock parser examines every fixed slot, including sparse slot IDs.
 * A zero count is no contacts, as confirmed by the A03 idle wire packet.
 * On invalid arguments/size/count, leave the caller's previous report intact.
 */
static inline int
a03_jd9365t_decode(const uint8_t *packet, size_t size,
    struct a03_jd9365t_report *out)
{
	struct a03_jd9365t_report next = {0};
	unsigned i;

	if (!packet || !out || size != A03_JD9365T_REPORT_SIZE ||
	    packet[0] > A03_JD9365T_CONTACTS) {
		return -1;
	}
	next.reported_count = packet[0];
	/* Hardware idle packet: count0, status byte2=FF, zero slot payload.
	 * Count remains metadata for positive sparse slots, but zero means no
	 * contacts. Never turn the idle zero coordinates into ten corner presses.
	 */
	if (!next.reported_count) {
		for (i = 0; i < 5u; i++) next.state[i] = packet[53u + i];
		*out = next;
		return 0;
	}
	for (i = 0; i < A03_JD9365T_CONTACTS; i++) {
		const uint8_t *p = packet + 3u + 5u * i;
		unsigned x = ((unsigned)p[0] << 8) | p[1];
		unsigned y = ((unsigned)p[2] << 8) | p[3];
		/* Match stock inclusive panel maxima; clamp only at HID conversion. */
		if (x <= 720u && y <= 1600u) {
			next.contacts[i].x = (uint16_t)x;
			next.contacts[i].y = (uint16_t)y;
			next.contacts[i].width = p[4];
			next.contacts[i].down = 1;
		}
	}
	for (i = 0; i < 5u; i++) {
		next.state[i] = packet[53u + i];
	}
	*out = next;
	return 0;
}

#endif

# A03 physical touchscreen bring-up

## Evidence and current boundary (2026-11-17)

The preserved BOOT0078 checkpoint renders the user-reported iOS clock and
SpringBoard reaches its application event loop. Physical touch and an unlocked
home screen remain unverified. Patch0145 supplies software HID event services
and explicit USB gestures; it does not drive the panel's physical digitizer.
Full Xcode CI43969089570 for exact2d4ffd7a44eab34178a13295b0ad3a337044e453
completed successfully on2026-11-16 at22:42:24UTC. This is build evidence only.

The A03 USB console returned later on2026-11-17. Old kernel input status
was unknown; the exact successful0145 artifact was then packaged as0079
and flashed to BOOT only at18:13UTC. USB returned18:14UTC; both HID services
registered and input status returned3. At18:16UTC both HID user clients
opened successfully and one explicit swipe-up dispatched down/move/up with
result0. Visible response and queue consumption remain unverified;
SpringBoard's latest sample was still startup.
See latest A03_PROGRESS.md/NOTES.md for runtime updates. Prior temporary
watchers were absent; this trial has its own image/manifest/capture.

## Controller selection

Private saved Android dmesg from2026-11-13 contains repeated successful
Jadard [JDTP] feature-command logs and the panel name
lcd_jd9365t_cpt_mipi_hdp. The matching Samsung HS03 driver maps that panel to
CPT_Jadard_firmware.bin and the JD9365T implementation (ROM ID constant0x9383).
This strongly identifies the Jadard/CPT path for the saved phone; it is not a
fresh read of the controller ROM ID under XNU.

The saved live DT places jadard@1 on spi3 at0x20150000, chip-select1, up to
10MHz, with panel720x1600 and10contacts. It also contains Chipone, Novatek and
GalaxyCore alternative nodes. Enabled DT nodes alone cannot identify the
fitted controller. Resolve GPIO phandles against that tree before programming
pins; raw specifiers are not interchangeable GPIO numbers.

Local primary source references (ignored vendor tree):

- drivers/input/touchscreen/HS03/jdchipset/jadard_common.c:
  panel/firmware selection, jadard_distribute_touch_data and
  jadard_parse_report_points.
- Same directory/jadard_common.h: TOUCH_DATA_LEN60, JD_ZERO_FLASH,
  coordinate offset3, ten five-byte slots, state offset53.
- Same directory/jadard_ic_JD9365T.c: jd9365t_ReadTpInfoBuf reads the
  firmware-discovered coordinate_report address; section discovery and
  firmware startup must precede using that address.
- drivers/spi/spi-sprd.c: the actual UNISOC SPI controller path.

## Prepared decoder

shim/a03/jd9365t-report.h decodes a complete60-byte coordinate report into
ten fixed slots. It preserves the stock big-endian coordinates, sparse slot
indices and inclusive720/1600 bounds. Out-of-range slots indicate no contact;
a later HID adapter must turn previously active slots into releases and use
the existing HID boundary clamp. Count is metadata, not a packed-slot bound.
Malformed lengths/counts leave prior output intact.

The decoder has no MMIO, transport, firmware upload or kernel registration.
It is not staged into the current XNU profile. Never feed failed transfers
as zero-filled packets: (0,0) is valid. Only call for successful coordinate
reads from a running controller, not gesture/debug events. The stock parser
does not establish packet integrity or freshness.

Run python3 tools/a03-test-jd9365t-report.py for C11/C++17 ASan/UBSan checks:
big endian, sparse/ten contacts, motion/release, edge coordinates, state bytes,
invalid lengths/counts and nulls. These synthetic reports do not prove
hardware operation or HID queue consumption.

## Next device checkpoints

1. Re-establish USB identity and inspect the actual running kernel. Package
   the exact successful0145 artifact only if needed, preserving the0078
   configuration except a03_hid=1 and retaining0078 as restore.
2. Verify HID provider registration, backboardd client open, then one explicit
   USB swipe and physical UI response as described in a03-usb-input.md.
3. Bring up bounded UNISOC SPI3/GPIO/clock access and read the Jadard ROM ID.
   Keep controller reset separate from display handling: this is an integrated
   display/touch part and the visible clock checkpoint must remain recoverable.
4. Account for the stock JD_ZERO_FLASH RAM-firmware path. Obtain the matching
   CPT firmware privately and verify its identity; do not assume S-Boot loads
   touch firmware because it initializes the display. Implement RAM loading
   and section discovery only after validating the controller/bus. Never
   reuse the vendor driver's external-flash erase/program routines.
5. Read/validate contact reports, adapt slot transitions to the existing HID
   provider, and verify down/move/up physically at all display edges. Failed
   reads must not synthesize presses; define bounded retry/release handling
   before enabling input. Preserve recovery, bootloaders, GPT and EFS/NV.

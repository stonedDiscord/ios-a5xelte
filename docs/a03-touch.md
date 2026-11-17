# A03 physical touchscreen bring-up

## Evidence and current boundary (2026-11-17)

BOOT0079 reaches the physically reported home menu after an explicit USB
Home-button press/release (~18:23UTC2026-11-17). A USB swipe while SpringBoard
was visible had no reported effect; physical finger touch remains unsupported.
The preserved BOOT0078 checkpoint renders the user-reported iOS clock.
Patch0145 supplies software HID event services
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
Later, after the user confirmed SpringBoard visible, a second USB swipe
dispatched successfully but produced no reported reaction. One following
USB Home event logged Menu0x40 down/up with one client; the user immediately
reported the home menu. Button UI response is supported; digitizer consumption
and touch gesture policy remain unresolved. No physical driver is enabled.
See latest A03_PROGRESS.md/NOTES.md for runtime updates. Prior temporary
watchers were absent; this trial has its own image/manifest/capture.

BOOT0080/0146 now confirms fresh XNU SPI3 ROM ID9383 on2026-11-17 at19:04UTC.
Explicit ROM probe returns0 and restores gate0A02DE00/clock0; inherited pins,
reset and CS0 work at1MHz. No firmware/contact/physical-touch proof yet.

## First physical coordinate and measured idle packet

On0084 an explicitly aligned held finger near screen center produces slot0
at332,805 across300samples. Session-final release is cleanup; physical lift
is not proven by that event. Raw0085 idle report is0000FF followed by57zeros,
with count0 but all coordinate fields0.0153 must ignore slot payload on a
zero count and release held contacts, while preserving positive sparse slots
and genuine0,0 coordinates in a nonzero contact packet. Earlier0149/0152
incorrectly interpret idle as ten corner contacts. Never enable their HID
poll command; all hardware captures so far used log-only contacts.0153 full
CI44173996698 exact8963305 is running; physical motion/lift/UI pending.

## Display ownership during touch trials

BOOT0082 user reports app icons after explicit Home, and also corrects the
prior clock report: GUI pictures periodically appear before boot logs cover
them again. The fallback framebuffer serial logger shares the panel RAM with
AppleCLCD. This is a display ownership defect distinct from touch reports.
0151 stops only its glyph writes after a validated GUI surface is ready to
copy, while retaining every byte in the USB spool. Full Xcode CI44165152625 succeeded. On0084 the user physically confirms
the iOS picture remains visible with no boot-log overwrite; USB capture
continues.0082 still has the overlay.

## Hardware RAM startup verified (2026-11-17, 19:53 UTC)

BOOT0082/0148 stages the private79104-byte CPT candidate with valid0 and
loads it explicitly: result0, all seven hardware RAM CRCs passed before MCU
start. ERAM ready is nowA55A, config20002AD4/1028, report20011580/60,
720x1600/18x32. Backdoor exit and SPI gate/source restoration pass. Firmware
execution/configuration is now established; no physical contact/HID result
yet. Poll0149 and time0150 full CI44162912240 remains in progress. Firmware
RAM is volatile and must be restaged after reboot. Keep private binary ignored.

## Current trial status (2026-11-17, 19:38 UTC)

BOOT0081/0147 has ROM9383 transport success and an ERAM ready value2317,
which fails the requiredA55A marker. The diagnostic refuses configuration
pointers after this failure and restores the SPI gate/source. The user
physically confirms the clock/lock screen after this boot. BOOT0080 remains
the physically confirmed home-icons plus working-ROM checkpoint.

0148 adds explicit private firmware staging into bounded kernel RAM and a
separate validated controller RAM load. Full CI44159557034 is in progress;
no controller firmware has been uploaded or started. The candidate remains
revision8 CPT firmware, not byte-matched to installed revision5. The RAM
loader permits only validated PRAM/DRAM moves and exact stock startup/CRC
controls, including DMA command3; it has no external-flash program path.

0149 is prepared but excluded from the build profile until the loader trial.
The touch contacts command logs contacts only. The touch poll command forwards
those same fixed slots to the existing HID provider. Both are explicit, bounded
300-frame sessions requiring ROM9383, readyA55A, DRAM config720x1600/18x32
and a60-byte ERAM coordinate report. Three consecutive failed samples stop
the session; held contacts are released at completion or sample failure.
Helpers, actual callback and kernel C compile pass local checks. Physical
reports and iOS digitizer consumption remain unverified; button response
proves neither.

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

Patch0146 adds explicit USB worker commands touch status and touch rom.
Status reads only the SPI3 gate/source registers. ROM temporarily enables
SPI3 at1MHz from ext26MHz, saves/restores control and clock state and runs
the stock enter/read-ROM-ID/exit sequence. It refuses an already busy bus.
No reset, GPIO, pinmux or firmware writes are present. The stock SPI driver
selects hardwareCS0 for every logical device, including Jadard's logicalCS1;
this diagnostic mirrors that behavior. Host tests exercise wire bytes, FIFO
chunks, bounded timeout and register restoration; hardware results need CI
and BOOT testing. Run tools/a03-test-jd9365t-spi.py and
tools/a03-test-touch-probe.py. A failed ROM test does not identify the cause
(pins, supply, inherited reset state and protocol are not yet runtime-proven).

shim/a03/jd9365t-report.h decodes a complete60-byte coordinate report into
ten fixed slots. It preserves the stock big-endian coordinates, sparse slot
indices and inclusive720/1600 bounds. Out-of-range slots indicate no contact;
a later HID adapter must turn previously active slots into releases and use
the existing HID boundary clamp. Positive count is metadata, not a packed-slot bound; count0 is idle/no contacts.
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

## Offline firmware candidate

Local revision8 A035GXXS8CYG1 stock vendor contains79104-byte CPT firmware,
SHA2568ba14e32cdeacd6763a9700fd5340f9c91763afc2965231148f72f9c1ceea82d.
All seven stock move-table CRC16 values validate with the source polynomial
8005/initialFFFF. This is not matched to installed revision5 and has not been
loaded. Private artifacts remain ignored under research/a03-touch-firmware.
Use tools/a03-inspect-jadard-firmware.py FILE for offline JSON inspection and
tools/a03-test-jadard-firmware.py for synthetic regression. Inspector validates
source bounds, target wrap and CRC; it does not establish panel compatibility,
ROM identity or permission to load targets. No device access in either tool.

### Source-guided follow-up after ROM9383

First check whether inherited firmware is running before choosing a RAM load.
Stock ChipInfoInit uses ERAM20011000: ready16-bit LE A55A at+0,
DSRAM entries at+4 (16 entries, eight bytes each), ESRAM entries at+136.
Each entry is LE32 address followed by LE32 length. ESRAM entry2 identifies
the coordinate report; DSRAM entry3 identifies firmware configuration whose
first six bytes are LE16 X/Y limits and one-byte X/Y sensor counts. These are
firmware-discovered addresses, not fixed contact-buffer assumptions. Read
transport success, ready marker, bounds, lengths and configuration must all
be checked before publishing contacts. Stock coordinate parser has no proven
integrity/freshness field; IRQ/poll semantics need hardware validation.

If ROM fails, GPIO145 reset is AP GPIO641B0000 bank9/bit1 (bank stride80hex):
data+480, mask+484, direction+488 and input-enable+4A8. Read-only snapshots
must precede any change. Saved DT pin controller is64710000/qogirl6; source
pinctrl-sprd-qogirl6.c encodes global SPI matrix at offset14hex and common/
misc pads at40/440hex bases. AP GPIO indices are not pinctrl enum indices.
Do not select SPI pads or power rails by numeric resemblance or alternative
DT touchscreen nodes. Current0146 intentionally leaves these untouched.

Standalone shim/a03/jd9365t-sections.h implements the fixed offsets above;
run tools/a03-test-jd9365t-sections.py for actual C/C++ ASan/UBSan tests.
It is preparation only, not staged in0146. Address whitelist and actual
successful read/controller readiness remain caller responsibilities.

The unstaged jd9365t-contact-state.h adapter emits fixed-slot transitions and
releases held contacts after three consecutive failed/malformed reads. This
is preparatory policy: a valid report resets the failure counter; a failed
read never enters the coordinate decoder as zero bytes. It has no polling,
bus or HID integration. Test with a03-test-jd9365t-contact-state.py.

The unstaged jd9365t-memory.h transport restricts whole RAM ranges before
any transfer: PRAM00000000..0000FFFF and DRAM20000000..2000FFFF; ERAM page
20011000..20011FFF is read-only. No peripheral register writes accepted.
It uses240-byte data chunks and the hardware-verified backdoor SPI framing.
Caller must identify the controller and manage the diagnostic session; this
helper neither loads firmware nor changes MCU state. Run its actual helper
regression with tools/a03-test-jd9365t-memory.py.

The unstaged jd9365t-firmware.h validator checks every move and CRC before
any future load:80KiB total, command0, bounded source/PRAM/DRAM targets,
nonoverlapping targets, all section CRCs. It has no device access. Run
its C/C++ regression with tools/a03-test-jd9365t-firmware.py and optionally
pass a private candidate file; successful parsing does not prove compatibility.

## Explicit temporary RAM trial (0148)

BOOT0081's section read returned ready2317 rather than A55A, after a good
ROM9383 read.0148 adds kernel-RAM upload staging and a separate explicit
RAM-only loader, following stock HostWritePram. Firmware stays private:

    python3 tools/a03-usb-touch-firmware.py PRIVATE.bin --log LIVE_CONSOLE.log

The sender waits for acknowledgement+workerEND on every chunk and validates
fwstatus. It never sends load. Only after a verified0148 kernel is booted,
issue touch load explicitly; the kernel revalidates the entire image and ROM,
checks hardware CRC per RAM section and starts MCU only after every section
passes. No external-flash program/erase, GPIO/pinmux or phone filesystem
write is implemented. A valid candidate still needs correct panel identity;
revision8 stock extraction is not a match to the installed revision5 image.

# A03 XNU USB console

Experimental opt-in a03usb_console=1 in patch0103. A03/T606 MUSB peripheral
code; existing screen remains active. No storage operations are added.

Framebuffer serial callback spools256KiB, overwriting oldest bytes on full.
Single-core profile masks IRQs in producer/consumer. BSD thread polls full-
speed PIO control/CDC endpoints; no USB DMA/IRQ routing. Host OUT discarded:
log output, not a shell. USB unavailable before BSD initialization and not
guaranteed after panic stops scheduling. USB reset does not rewind logs.

Matching local Linux Qogirl6 sources ground AON0x64000000, analog0x64570000,
MUSB0x64900000; OTG/UTMI reference clocks, analog power,16-bit UTMI,
peripheral ID, device eye pattern0x04f3d1c0,25ms PHY reset. PMIC regulator
state preserved: powered-down supply can block enumeration. No partition
changes added. Diagnostic VID1d6b/PID0104 serialA03XNUConsole01 is private
bring-up identity only. Linux cdc_acm should expose /dev/ttyACM*.

Capture verifies exact VID/PID/serial and uses raw1152008N1:

    python3 tools/a03-usb-console.py --wait 120 --duration 300

Default output is private shim/a03/out/. Grant only detected tty permissions
if needed. Baud is a CDC control value, not physical UART speed.

    python3 tools/a03-test-usb-console.py

Host-only checks cover staged patch descriptors/interfaces/endpoints,
control device/configuration/string/address/config/CDC requests, stalls,
exact64-byte completion. Local three-component kernel syntax and patch
roundtrip checks pass. Driver/spool use general-register codegen. Hardware
PHY/USB enumeration/packet transfer and panic service remain unproven.

Startup waits up to10seconds for configuration, then1second for drain,
before continuing toward initproc. This does not guarantee panic output.

## Post-trap monitor

Opt-in a03debug_hold=1 (0104) pauses the current PID1 SIGTRAP fatal exit
before coredump/panic. This preserves that thread's map for copyin while
letting the scheduler/USB worker run. It is not a recovered userspace shell,
LLDB, arbitrary task execution or launchd restart. Other exit paths still
follow existing behavior. USB itself must enumerate first.

    python3 tools/a03-usb-console.py --interactive
    python3 tools/a03-usb-console.py --command regs --command 'mem 12345678 40'

Commands: help, regs, bt, mem HEXADDR [HEXCOUNT], panic. Memory reads use
current dying initproc map, at most0x100 bytes, copyin errors reported.
regs/bt print existing saved registers and six frames. panic leaves the hold
and continues normal fatal exit/coredump/panic; it does not resume userspace.
No memory/register writes or partition operations. One pending command slot.
Opt out by omitting the boot arg; no filesystem change needed.

    python3 tools/a03-test-usb-monitor.py

Host parser/queue checks, patch roundtrip and three affected source syntax
compiles pass. Runtime survival/USB responsiveness remain unproven.

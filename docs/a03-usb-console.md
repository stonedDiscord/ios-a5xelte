# A03 XNU USB console

Experimental opt-in a03usb_console=1 in patch0103. A03/T606 MUSB peripheral
code; existing screen remains active. No storage operations are added.

Framebuffer serial callback spools256KiB, overwriting oldest bytes on full.
Single-core profile masks IRQs in producer/consumer. BSD thread polls full-
speed PIO control/CDC endpoints; no USB DMA/IRQ routing. Patch0104 routes host OUT to the bounded diagnostic monitor described below. USB unavailable before BSD initialization and not
guaranteed after panic stops scheduling. USB reset does not rewind logs.

Matching local Linux Qogirl6 sources ground AON0x64000000, analog0x64570000,
MUSB0x64900000; OTG/UTMI reference clocks, analog power,16-bit UTMI,
peripheral ID and25ms PHY reset. Patch0106 selects the matching board trim
0x04b3d1c0 and explicitly clears host pulldowns. PMIC regulator
state was inherited through0106;0109 explicitly enables the verified USB rail. No partition
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

## BOOT0047 hardware evidence and next PHY candidate

Startup reaches CDC initialized, but host100-second capture sees no USB
attach. No enumeration or interactive monitor success is established.
Patch0106 uses matching ums9230-25c10 device trim04b3d1c0 instead of generic
04f3d1c0. It mirrors sprd_hostphy_set(peripheral): REG_SEL_CFG_0+20 bits6,
UTMI_CTL2+c clear18 pulldowns, UTMI_CTL1+4 clear low16 reserved bits.
Readbacks print trim/CTL1/CTL2/select, MUSB power/devctl/version and ten-second
reset/setup counts. Regulator state is still inherited; no PMIC writes.
These changes require a new kernel and physical enumeration evidence.

## Source audit and USB candidate0109 (2026-11-15)

The prior initialized message proves software setup only. Matching Linux
sources identify three gaps in that setup:

- phy-sprd-qogirl6.c probe enables ANA_EB (AON EB1 bit12), in addition to
  OTG_UTMI_EB bit8. The earlier XNU implementation only enabled bit8.
- PHY init sets and enables SC2730 VDDUSB33 at3300000uV. Inherited supply
  state was never verified in XNU. Live DT selects the sharkl5 ADI fallback
  (0x64200000 controller,0x20000 slave window, address-echo read validation).
- musb_sprd.c declares MUSB_DMA_SPRD without MUSB_INDEXED_EP. musb_core.c
  therefore uses flat endpoint registers at0x100+16*ep+register, whereas
  earlier XNU code used the indexed0x10 aperture. FIFO sizing stays indexed.

0109 enables the missing gate, reads the USB supply, unlocks regulator writes
only if needed, sets VDDUSB33 selector210 (1.2V+210*10mV), clears its power-down
bit and verifies readback before attaching. ADI writes are allowlisted to
0x1bd0 unlock,0x19e8 USB power-down and0x19ec USB voltage; no other rail,
reset, watchdog or storage operation is exposed. Polls have bounded timeouts;
failed map/address echo/readback stops console startup with a diagnostic.
Live DT has no ADI hwlock; existing bootloader ADI timing/channels remain.

Also selects USB on the documented shared pin mux (AON0x374 low4 bits), clears
vendor HOST_FORCE_EN (MUSB0x34b bit0), detaches for20ms, and uses Linux's flat
endpoint layout for EP0, bulk and interrupt endpoints. This is a candidate
fix until an actual host attach/configuration/tty transfer is captured.

    python3 tools/a03-test-usb-console.py
    python3 tools/a03-test-usb-supply.py
    python3 tools/a03-test-usb-monitor.py

Host tests cover actual cumulative source, flat endpoint address isolation,
CDC protocol/commands, supply write allowlist/preserved bits/no-op state,
bounded busy/FIFO timeouts, bad address echo and failed physical readback.

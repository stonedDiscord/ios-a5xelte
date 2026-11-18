# DREAMLTE USB bring-up evidence

##0217 endpoint command snapshot (2026-11-18)

Phone reports ep0 cmd1 reg00000401; PAR0=00000200/PAR1=00000500/PAR2=0;
GCTL80e92004/GSTS3e800000/USB2=40102400; DCTL0/DSTS00520000/DALEPENA0.
CMDACT remains set, so this is incomplete SETEPCONFIG, not status0 success.
Parameters encode64-byte OUT EP0 with expected events. Device mode is2;
USB2 reset/SUSPHY/ENBLSLPM and GSTS CSR timeout are clear. Stopped/halted
state is expected before the later RUN request. No USB enumeration proof.
0218 follows Samsung resource-before-config ordering; full CI44261810052
succeeded and BOOT0218 is now installed; physical result pending. Prior GHWPARAMS3=10420085 has16 IN/16 OUT, within candidate bounds.

## Current diagnostic trial (2026-11-18)

Latest:0219 exact CI44265115339 at41f5575 SUCCESS; nine source hashes,
six symbols and fourteen linked diagnostic strings verified. Fresh Download
Mode050 accepted BOOT0219 (100%, exit0/reboot). No host1209:0001 gadget;
physical four FAIL, one CORE and two PHY lines requested. No runtime PHY
or USB pass. Earlier0218 trial details below remain historical context.


0218 exact CI44261810052 at94e4d74 succeeded. Nine compiled sources,
six linked symbols and eleven diagnostic strings verified; BOOT uploaded
100%, Heimdall exit0/reboot. Host still sees no1209:0001 gadget; physical
resource-assigned or endpoint-failure report is pending. The resource-order
change follows Samsung gadget.c but has no demonstrated hardware success.
Earlier version/PE_lockdown_iokit apparent stops are superseded by physical
0215/0217 output reaching USB setup and Apple_HFS root discovery.

Prepared0219 outside active profile adds failure-only reads of DWC3 PIPE,
GHWPARAMS3 and bus config, plus the already-mapped PHY bank LINK/UTMI/CLK,
PHYRESUME(Q) and PHYSELECTION. Pinned Samsung CAL forces QACT and pulses
link reset before endpoint setup; the current takeover path does neither.
This source difference is a hypothesis, not proof of a clock fault. Read
those fields before changing Q-channel/port/reset behavior. No additional
MMIO writes or mappings in0219; actual ARM64 compile and modeled suites pass.

## Physical framebuffer evidence (2026-11-18)

Verified0214 BOOT flashed successfully and the user reads
`SWEET USB: endpoint 0 setup failed` on the phone. This establishes normal
XNU framebuffer output and execution past the DCTL soft-reset guard into
the five-command EP0 configuration sequence. The preceding command/status
or timeout line is required to isolate the failing operation. No host gadget
is present. Do not infer a working PHY, DMA or enumeration from this message.

0215 adds Samsung core.c USB2 ENBLSLPM/SUSPHY clearing and post-reset
66MHz GCTL timing; commit5439710, full CI44256127913 succeeded. Actual
wrapper host tests pass again on2026-11-18. Reviewed gadget.c uses the same
EP command register layout, CMDACT/status fields and EP0 configuration bits;
the failure is not yet evidence of an incorrect register address.

The target is a USB connection from the running S8 shim/XNU, with host-side
transfer verification. Android ADB recovery of last_kmsg is diagnostic support;
it does not meet that target.

## Measured controller state (2026-11-17)

Live DT identifies DWC3 at `0x10c00000`, IRQ SPI337 (INTID369), PHY windows
`0x10e00000+0x100` and `0x10e10000+0x100`, and a reference-clock selector
at `0x10e50070+0x10` (offset0xc, mask/value0x1000000). DWC3 clocks are
`aclk`/`sclk`; PHY clocks are `ext_xtal`/`aclk`. Both nodes declare
`is_not_vbus_pad`. DT permits SuperSpeed; current Android USB is high-speed.

The0210 pre-XNU snapshot and current Android debugfs regdump differ:

| Register | Loader0210 | Android configured |
| --- | --- | --- |
| GSNPSID | 0x5533280a | 0x5533280a |
| GCTL | 0x30c12004 | 0x80e92004 |
| DCTL | 0x00000000 | 0x8c000000 |
| DSTS | 0x00520004 | 0x00825188 |
| DCFG | 0x00080804 | 0x004808d4 |

Android also reports `GUSB2PHYCFG(0)=0x40102540`,
`GUSB3PIPECTL(0)=0x110c0002`, `GSBUSCFG0=0x22220009`,
`GSBUSCFG1=0x300`, `DALEPENA=0xf`. Its event ring has a nonzero upper
address word (`0x8`), so the working Android controller can DMA above4GiB.
This does not prove all shim DMA choices or XNU cache attributes are valid.
The private complete dump is in the ignored S8 backup directory. Do not
reuse Android's event-ring or endpoint DMA addresses after replacing Linux.

Loader DCTL.RUN_STOP is clear and DSTS.DEVCTRLHLT is set. Core register
access works, but this does not establish PHY readiness or an active USB link.

## Exynos-specific source reference

Reviewed Linux source from
[exynos8895/android_kernel_samsung_universal8895](https://github.com/exynos8895/android_kernel_samsung_universal8895/tree/3cfb914658ab077aef9ed500aa4a583782971fbf),
lineage-19.1 commit `3cfb914658ab077aef9ed500aa4a583782971fbf`:

- `drivers/usb/dwc3/dwc3-exynos.c`: Exynos8895 clock wrapper.
- `drivers/phy/phy-exynos-usbdrd.c`: selects PHY version01.1.1,
  CLKCORE reference, second register bank, GPIO-selected port and optional
  tuning. Power-on separately removes PMU isolation.
- `drivers/phy/phy-samsung-usb3-cal.c`:
  `samsung_exynos_cal_usb3phy_enable` checks the PHY version register and
  may advance the register base by4; sets q-channel/mux/reference clock;
  asserts port reset, delays10us, releases reset, delays500us; releases
  force-sleep/suspend and DP/DM pulldowns. With `is_not_vbus_pad`, it sets
  LINKSYSTEM FORCE_BVALID/FORCE_VBUSVALID and PHYUTMI VBUSVLDEXTSEL/
  VBUSVLDEXT. It clears DRVVBUS and sets OTGDISABLE. These settings are
  different from the donor Qualcomm QSCRATCH VBUS override.

These sources locate the required sequence; they are not proof that the
current phone runs precisely this source revision. Before a new PHY write
trial, inspect its register layout/version and preserve the device-specific
clock, GPIO port and reference selection. A blind copy of the S7, Qualcomm
or UNISOC initialization is not a validated Exynos8895 implementation.

## Next implementation gates

First recover reliable XNU output across the VM switch (0211 CI/trial).
Then implement S8 core/PHY initialization and a polled DWC3 gadget using
owned DMA buffers and explicit cache maintenance. The existing
`0073-sweet-usb-device-ep0.patch` provides a DWC3 control-transfer reference;
its Qualcomm clock/PHY accesses are not S8 code. Verify host enumeration,
control transfers, and bidirectional data while shim/XNU is running before
claiming working USB. Preserve all non-BOOT partitions.

## Opt-in ECM candidate0212

Overlay0212 enables the inherited polled DWC3 CDC-ECM transport for DREAMLTE
and starts it after BSD network initialization, before root-device discovery.
It never calls the donor UFS initialization or its disk-backed log stream.
`dreamlteusb=0` (default) performs no controller accesses; `=1` reports core
state; `=2` attempts firmware-state takeover for the measured DWC3 ID only.
It refuses a running core, PHY port reset or forced sleep/suspend. It sets
DWC3 device mode and uses the Exynos PHY VBUS masks above. Cold PHY clock/
isolation/reset initialization still needs device evidence and implementation.

The candidate initializes USB2 EP0 with64-byte packets and rejects malformed
or oversized event counts. Existing ECM configuration uses kernel interface
`ue0` at192.168.7.2/24; a host must configure192.168.7.1/24. Enumeration and
bidirectional transfer (for example ARP plus ping) must be measured on S8.
No runtime success is claimed from compilation or host modeling.

## Source-derived cold-start register map (2026-11-17)

Further review of the same pinned Linux revision resolves the clock and
isolation dependencies below. These addresses are implementation references;
none of these new clock/PMU writes has been tested on XNU.

| Dependency | Physical address / field | Source |
| --- | --- | --- |
| USB DRD isolation release | PMU `0x16480704`, bit0 set | live PMU node; phy-exynos-usbdrd.h and pipe3_phy_isol |
| PHY reference selector | `0x10e5007c`, bit24 set | live usbphy-refclk and change_refclk |
| FSYS0 USB clock user mux | `0x11000180`, select bit4, busy bit16 | cmucal-sfr.c / cmucal-node.c |
| USB link Q-channel | `0x11003044`, enable bit0, request bit1 | cmucal-sfr.c / clk-exynos8895.c |
| USB ACLK gate | `0x11002078`, manual bit20, value bit21 | cmucal-sfr.c |
| USB reference gate | `0x1100207c`, manual bit20, value bit21 | cmucal-sfr.c |
| USB suspend gate | `0x11002080`, manual bit20, value bit21 | cmucal-sfr.c |
| Upstream USB clock mux/divider/gate | CMU `0x15a81068` / `0x15a81864` / `0x15a8206c` | cmucal-sfr.c |

Live DT clock IDs `0x2ca` and `0x2bf` select GATE_USBTV_USB30DRD_LINK
and USBDRD30. PHY version01.1.1 uses CLKCORE, common_block_disable=false,
and an initial port0 selection overridden by the board GPIO. Do not infer a
port from cable orientation alone. PHY register-version adjustment shifts
both banks by4 when the first version word is nonzero.

The CAL sequence first handles Q-channel and link reset, preserves/selects
the PHY port mux, configures reference source/frequency under PORTRESET,
waits10us before releasing reset, powers both PHY banks for1ms then powers
down the unused bank, waits500us, releases sleep/suspend/pulldowns, and sets
the device VBUS overrides. PHYRESUME Q-channel forcing has500us delays;
it is separate from the FSYS0 clock-controller Q-channel above. Full cold
initialization must also retain board tuning and upstream clock rates.
Candidate0213 only attempts the already-awake PHY path; a refusal is not
evidence of broken USB endpoints. Framebuffer0214 is intended to expose
that refusal or an earlier kernel failure without restoring Android.

Host wrapper check against a staged source tree:

    python3 tools/dreamlte-usb-host-test.py PATH/TO/xnu/bsd/dev/sweet_usb.c

The test compiles the actual wrapper/PHY functions with modeled MMIO. It
checks default-off/read-only behavior, ID/running/reset/suspend refusal,
version-dependent register offsets, preserved control bits and VBUS masks.
It does not emulate the DWC3 endpoint/DMA engine or test PHY electrical state.
0211 must first be flashed/recovered using its own exact CI artifact; do not
claim that its kernel contains0212 merely because the local profile does.

Overlay0213 retains snapshot output after pmap bootstrap and registers a
RAM-backed serial console so normal kernel printf reaches the same bounded
buffer during BSD/USB setup. Snapshot aliases use LOW_GLOBAL_BASE_ADDRESS
plus2MiB/4MiB, within the reserved low-globals range. VM_MIN_KERNEL_ADDRESS
is a different L1 range on this4K non-large-memory kernel and is unsuitable.
No framebuffer, UART or storage accesses are needed for this console.

For a running gadget, `python3 tools/dreamlte-usb-check.py` issues real EP0
GET_DESCRIPTOR/GET_STATUS/GET_CONFIGURATION requests. After configuring the
host ECM interface at192.168.7.1/24, add `--interface NAME` to require its
USB parent/MAC identity and three ICMP request/reply exchanges. This helper
has only been checked for syntax/help and correct absence reporting so far;
no running S8 gadget has passed it yet.

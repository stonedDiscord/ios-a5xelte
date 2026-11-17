# DREAMLTE USB bring-up evidence

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

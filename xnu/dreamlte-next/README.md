# Prepared S8 USB follow-up

Current2026-11-18:0216 promoted into active xnu/dreamlte with0217 startup
checkpoints after user reports startup trace ending at PE_lockdown_iokit.
Four actual ARM64 files compile; exact0215 source plus plain patches matches
all four reviewed files. Full CI required; no new runtime claim. Earlier
outside-profile status below is preparation history.

0216-dreamlte-usb-ep-failure-snapshot.patch stays outside the active profile.
It adds failure-only readbacks of the endpoint command/parameters, GCTL,
GSTS, USB2PHYCFG, DCTL, DSTS and DALEPENA. No retries or recovery writes.
Plain patch application, actual ARM64 USB translation-unit compilation and
actual-function modeled completion/status/timeout tests pass. Not built into
CI44256127913 and not flashed; only promote if0215 still needs diagnosis.

Run tools/dreamlte-usb-epcmd-test.py against a staged sweet_usb.c to check
the command flow and failure snapshot's absence of additional MMIO writes.

2026-11-18 update:0215 moved to active xnu/dreamlte at5439710. Full build
CI44256127913 is pending;0214 has now flashed and displays the XNU message
`SWEET USB: endpoint 0 setup failed`. The preparation history below describes
the earlier staging state, not current patch location or runtime success.

0215-dreamlte-usb2-link-clock.patch is intentionally outside the active
dreamlte profile. CI44119574729 builds0214 for the framebuffer trial; do not
claim that artifact includes0215 or restart it merely because it is queued.

The pinned Exynos8895 Linux drivers/usb/dwc3/core.c provides two concrete
missing steps in the existing firmware-state takeover path:

- dwc3_phy_setup clears USB2PHYCFG ENBLSLPM bit8 and SUSPHY bit6.
- dwc3_core_soft_reset/reset_check programs GCTL PWRDNSCALE bits19..31
  from live-DT suspend_clk_freq66000000 /16000 =4125, and clears bits6/7.

This candidate preserves board PHYIF/turnaround and other control fields,
refuses core/USB2 PHY reset, wakes the USB2 interface before DCTL reset and
programs the timing after reset. It does not implement cold PMU/CMU/PHY
power/reset initialization, nor claim physical enumeration.

The actual wrapper host check supports both0214 and0215. It verifies reset
refusal, preserved USB2 configuration bits and every GCTL bit against the
source-derived timing mask. 0x30c12004 becomes0x80e92004, matching the prior
working Android register dump. That match is supporting evidence, not an XNU
device result. Plain git apply/full-source equality also passes; reviewed
next sweet_usb.c SHA256:
df5d49b67402780ee2b3f347197b80c407a4c81598593cb8916082cda262770b.

After the0214 display trial, promote this patch to xnu/dreamlte, update the
USB source hash and linked-symbol expectations, and run full CI before a
USB follow-up trial. First use framebuffer output to distinguish an early
kernel fault, cold-PHY refusal, DCTL reset timeout and endpoint setup failure.

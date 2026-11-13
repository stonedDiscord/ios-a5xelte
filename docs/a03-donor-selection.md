# A03 donor choice: native 16 KiB, SWEET core and Topaz improvements

Assessment date: 2026-11-13. This is a source-selection decision, not a
completed replacement build profile or an XNU boot result. Keep the
working A03 probe and restore checkpoint on `a03-bringup`.

## Verified hardware basis

Pre-Linux probe 0001 read MMFR0 0x101122 on the boot Cortex-A55. Its
TGran16 field is 1 (supported), TGran4 field 0 (supported). Prefer a
native 16 KiB XNU for initial A03 bring-up. We have not yet installed
16 KiB translation tables or sampled the two A75 CPUs before Linux.
Validate translation and every additional CPU before claiming 16 KiB SMP.

A03 live DT has GICv3 and PSCI/SMC. SWEET's native 16 KiB/GICv3 direction
fits this better than continuing the Exynos HEROLTE/A5XELTE 4 KiB/GICv2
adaptation. The A03 enters at EL2, whereas the inspected SWEET/Topaz shim
expects EL1; our own EL2 setup is still required.

## Pinned upstream sources inspected

- Core reference: `dipa-studio/ios-sweet`, main commit
  `45263bee51df4a0f55cdf9c649af886399488ddb`.
  https://github.com/dipa-studio/ios-sweet/tree/45263bee51df4a0f55cdf9c649af886399488ddb
  README and `xnu/patches/0004-sweet-machine-config.patch`: XNU 8796,
  iOS 16.7.16 userland, plain arm64, ARMv8.2 build, 16 KiB and GICv3.
- Integration donor: `MakrSas/ios-topaz`, topaz commit
  `e4772911e116ab4ab6c4ac1f38e6106fefe8b483`.
  https://github.com/MakrSas/ios-topaz/tree/e4772911e116ab4ab6c4ac1f38e6106fefe8b483
  README, workflow, shim entry and patches 0140/0141 inspected. Its
  workflow also uses macOS 13.5/XNU 8796. README reports UI, Wi-Fi, Adreno
  acceleration, sound and charging; these are upstream claims, not A03
  observations. README has older Gold-only/16K sections alongside newer
  eight-core claims: inspect build flags and code, not headline alone.
- Additional reference: `PixOS-Project/pixelios-kernel` README, main as
  retrieved on 2026-11-13. Tensor G1/iOS 16 port; no pinned code selected.
  https://github.com/PixOS-Project/pixelios-kernel

## Adaptation rules

1. Target native 16 KiB, single boot A55 first, plain arm64. Retain A03
   BOOT v2 packaging and its returning-probe checkpoint. Do not use the
   existing dreamlte/HEROLTE workflow profile for an A03 kernel.
2. Use the native SWEET core as the architectural baseline and review
   Topaz's later generic IOSurface, IOKit and userland compatibility work
   as the richer donor. Record exact imported patches and dependencies.
3. Leave `TOPAZ_4K` disabled: Topaz patch 0140 makes 4 KiB optional and
   patch 0141 enables AMP under that flag to support its A53 cluster.
   That workaround is not a requirement for the observed A03 boot A55.
4. Replace all board constants and early display writes before building
   a runnable A03 profile. Timer INTID is 27 here, not SWEET's 19;
   GIC addresses, reserved RAM, EL2 setup and storage are A03-specific.
5. Topaz's Qualcomm modem/Wi-Fi, Adreno/Mesa driver, sound, clock, power
   and display routines cannot be enabled on UNISOC by copying patches.
   Live A03 DT identifies `sprd,mali-natt` GPU, not Adreno. Generic
   surface/compositor interfaces may be reusable after driver review.
6. Keep XNU generation and donor maturity separate: both inspected
   upstreams are XNU 8796/iOS 16. Native 16 KiB support alone does not
   establish compatibility with iOS 17/18 or another XNU generation.

## Next execution checkpoint

Use the cloned stock kernel's EL2 setup and live DT to verify EL1 entry
and an actual 16 KiB mapping in a returning probe, then timer/GIC IRQs.
After that, implement a separately named A03 16 KiB build profile with
the pinned donors and no unreviewed peripheral initialization. No kernel
build, source rebase, donor-image flash or iOS version upgrade occurred
as part of this assessment.

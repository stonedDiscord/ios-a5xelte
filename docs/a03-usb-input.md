# A03 USB input trial

BOOT0079 runtime2026-11-17: both services registered/opened; input status3.
A USB swipe on visible SpringBoard dispatched with result0 but had no user-
reported reaction. A following USB Home press/release (Menu0x40, one client)
was followed immediately by the user's physical home-menu report. This
establishes a button/UI milestone; physical touch remains unsupported.

For physical digitizer evidence and the separate Jadard hardware work, see
[a03-touch.md](a03-touch.md). The0145 full Xcode CI43969089570 completed
successfully for exact2d4ffd7 on2026-11-16; runtime delivery remains unverified.

The first physical iOS clock screen is BOOT0078 (2026-11-16). That kernel
has no HID provider and cannot deliver touch or Home input. Preserve its
verified image and manifest as the rendering checkpoint.

Patch 0145 adds portable IOHID event/queue services from donor patch 0058.
It includes no donor MMIO, hardware touch controller or button driver.
Registration requires exact boot argument a03_hid=1; the default is off.
Backboardd's matching signed XML has the required boolean entitlement
com.apple.hid.system.user-access-service.

A new kernel must pass full Xcode CI and be packaged/verified before flashing
only the authorized A03 BOOT partition. Retain the original RAM, loader,
ADT, root and stock DT settings. Do not enable optional lab vault patch 0144
as part of this input-only trial.

Keep one USB console reader running, then use EP0 without opening the tty:

    python3 tools/a03-usb-input.py status
    python3 tools/a03-usb-input.py home
    python3 tools/a03-usb-input.py swipeup

Status result is a provider bitmask: 1 buttons, 2 touch. Home emits one
80ms consumer Menu press and release. Swipe emits one finger at x360 from
y1560 to y460 over 336ms, then releases. Coordinates use the 720x1600 display.
No timer emits automatic input. Commands execute in the dedicated probe
worker; a gesture briefly occupies that worker, not the USB polling thread.

A successful EP0 transfer means queued. Kernel result 0 for an action means
the action function dispatched its sequence; it does not prove allocation,
client acceptance, queue consumption, unlock or a rendered home screen.
Inspect provider registration, backboardd's successful client open, event
logs and physical display response before claiming delivery or completion.
If a passcode or setup screen appears, report that state accurately.

Local checks:

    python3 tools/a03-test-usb-input.py
    python3 tools/a03-test-hid-touch.py

The first test exercises actual action bodies with host callbacks. The
second exercises the actual touch-builder body with host event objects,
covering normalization, masks, duplicate suppression and release. Neither
proves the kernel/userspace ABI. Full local C++ syntax checks require host
stand-ins for unavailable Apple allocation builtins; those stand-ins must
never enter CI or a bootable kernel. Full Xcode build and runtime checks
remain required.

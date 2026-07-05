# SettingsQR

> Configure your SeedSigner in one scan — encode your preferred settings in a QR code and apply them instantly.

SeedSigner deliberately forgets: with the SD card removed, settings changes live only in RAM and are gone at power-off. That's great for security and tedious for configuration — re-enabling testnet, your coordinator, BIP-85, and your camera rotation through the menus on every boot gets old fast.

**SettingsQR** solves this. You describe your preferred configuration once in a QR code; from then on, a single scan applies the whole configuration in seconds.

## Create your SettingsQR

Use the official web generator:

**[https://seedsigner.github.io/seedsigner-settings-generator/](https://seedsigner.github.io/seedsigner-settings-generator/)**

1. Open the generator and set each option the way you want it — the choices mirror the device's own [basic](/reference/settings/basic.md), [advanced](/reference/settings/advanced.md), and [hardware](/reference/settings/hardware.md) settings menus.
2. The page renders a QR code that updates live as you change options.
3. Save it: print it, or keep a screenshot/PDF wherever you keep the device.

> **Tip:** A SettingsQR contains **only configuration:** no seed material, no keys. It is safe to print, photograph, and leave next to the device. (Someone who sees it learns your preferences, such as which network and coordinator you use, but nothing secret.)

## Apply it on the device

1. From the main menu, select **Scan**.
2. Point the camera at your SettingsQR.
3. SeedSigner recognizes it as a settings payload, applies the configuration, and confirms what changed.

That's it — no menu digging. If an SD card is inserted, the settings also persist to the card as usual; if you run card-free, rescan after each boot.

## When it's most useful

- **Card-free operation.** You remove the SD card for security ([why](/reference/device/first-boot.md#remove-the-sd-card-for-maximum-security)), so nothing persists — one scan restores your full setup each session.
- **Multiple or borrowed devices.** Apply an identical configuration to every SeedSigner you touch.
- **Testnet practice.** Keep two SettingsQRs — one for your testnet practice profile, one for your mainnet profile — and switch with a scan. See [Using testnet](/contribute/testnet.md).
- **Recovering from experiments.** Fiddled the settings into a weird state? Scan your known-good QR to get back.

> **Warning:** Only scan SettingsQRs you created yourself or fully understand. A settings payload can flip security-relevant options (network, warnings, enabled features) — review the confirmation screen after scanning.

## Related pages

- [Basic settings](/reference/settings/basic.md), [Advanced settings](/reference/settings/advanced.md), [Hardware settings](/reference/settings/hardware.md): what each option does.
- [First boot](/reference/device/first-boot.md): why running without the SD card is recommended.

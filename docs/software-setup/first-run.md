# First-run configuration

> Recommended settings to adjust on your first boot.

When SeedSigner boots for the first time, it starts with sensible default settings. Everything works out of the box, but a few quick adjustments will tailor the device to your setup.

## Recommended first steps

### 1. Set your coordinator software

Go to **Settings → Coordinator Software** and enable the wallet(s) you plan to use with SeedSigner. Supported coordinators include:

- Sparrow Wallet
- BlueWallet
- Nunchuk
- Specter Desktop
- Keeper

SeedSigner adjusts its QR code output format based on the coordinator you select, so setting this correctly ensures smooth communication between your signing device and your wallet software.

> **Tip:** If you're not sure which coordinator to use, Sparrow Wallet is a popular choice for desktop users. It has excellent support for SeedSigner and multisig setups.

### 2. Decide on persistent settings

Go to **Settings → Persistent Settings** and choose your preference:

- **Enabled** — Your settings are saved to the MicroSD card and persist across reboots. Convenient if you use the same configuration every time.
- **Disabled** — Settings reset to defaults each time you power on. Nothing is written to the SD card, which is the more secure option.

This is a tradeoff between convenience and security. If you remove the SD card after boot (as described in the previous guide), persistent settings won't apply regardless.

> **Warning:** If persistent settings are enabled, your configuration preferences are stored on the SD card in plain text. This is not a risk to your keys, but it does leave a record of your settings on removable media.

### 3. Adjust camera rotation if needed

If the camera preview appears upside down, go to **Settings → Advanced → Camera Rotation** and change the rotation value. This is common depending on how your camera ribbon cable is oriented in the enclosure.

### 4. Verify your hardware

Go to **Settings → I/O Test** to confirm that the display, camera, and joystick are all working correctly. This quick test gives you confidence that your build is solid before you start handling real keys.

## All settings

These four steps cover the essentials. For a complete list of every option available, see the [Configuration Reference](/configuration/basic.md).

## Next steps

Your SeedSigner device is ready to go. Head over to [Create a new seed](/using-seedsigner/create-seed.md) to generate your first seed phrase.

> **Tip:** If you run into hardware issues during setup, the [I/O Test](/configuration/basic.md#hardware-io-test) and [Common issues](/troubleshooting/common-issues.md) pages can help you diagnose the problem.

# Basic settings

> Top-level settings for coordinator selection, display preferences, and hardware diagnostics.

**Navigation:** Main Menu > Settings

Most users only need to adjust a few of these to match their preferred wallet software and workflow.

---

## Settings reference

| Setting | Path | Description | Default |
|---------|------|-------------|---------|
| **Coordinator Software** | Settings > Coordinator Software | Select which wallet application you use: BlueWallet, Nunchuk, Sparrow Wallet, Specter Desktop, or Keeper. This controls which QR code formats SeedSigner generates, ensuring compatibility with your chosen coordinator. | — |
| **Denomination Display** | Settings > Denomination Display | Choose how Bitcoin amounts are displayed on screen. A threshold (default: 0.01 BTC) determines when amounts switch between BTC and sats notation. | Threshold: 0.01 |
| **Persistent Settings** | Settings > Persistent Settings | When enabled, your settings are saved to the SD card and survive reboots. When disabled, all settings reset to defaults every time the device powers off. | Disabled |
| **I/O Test** | Settings > I/O Test | Runs a hardware diagnostic that tests all buttons, the display, and the camera. Useful for verifying a new build or diagnosing hardware problems. | — |
| **Donation** | Settings > Donate | Displays information on how to donate to support ongoing SeedSigner development. | — |

---

## Details

### Coordinator software

SeedSigner can generate QR codes optimized for several popular wallet coordinators. Select yours so that exported QR codes scan reliably in your wallet app.

Supported coordinators:

- BlueWallet
- Nunchuk
- Sparrow Wallet
- Specter Desktop
- Keeper

> **Tip:** If you switch wallet software, come back here and update this setting so your QR codes are formatted correctly.

### Denomination display

Controls whether amounts are shown in BTC or sats. The threshold determines the crossover point — amounts below the threshold display in sats for readability, while larger amounts display in BTC.

### Persistent settings

This setting controls whether your configuration is written to the SD card.

- **Enabled** — Settings persist across reboots. Configuration data is stored on the SD card.
- **Disabled** — Settings reset to factory defaults every time the device powers off.

> **Warning:** Enabling persistent settings stores configuration data on your SD card. If your threat model requires leaving no trace on removable media, keep this disabled.

> **Tip:** If you find yourself reconfiguring the same settings every time you power on, enabling persistence saves time without exposing any seed data.

### Hardware I/O test

The I/O test walks you through each hardware component — press each button when prompted, verify the display renders correctly, and confirm the camera captures an image.

This is especially helpful when:

- You have just completed a new hardware build
- A button or the camera seems unresponsive
- The display shows unexpected behavior

### Donation

View a QR code and address to support the SeedSigner project. All development is community-funded.

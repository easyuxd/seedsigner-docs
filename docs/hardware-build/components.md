# Components list

> The parts you need to build a SeedSigner device — roughly $50, no soldering required.

Building a SeedSigner device requires just three core electronic components, a MicroSD card, and a power source.

## Core components

### 1. Raspberry Pi Zero v1.3

The Raspberry Pi Zero v1.3 is the main computer that runs SeedSigner. Version 1.3 is the ideal choice because it **physically lacks Wi-Fi and Bluetooth hardware**. There is no wireless radio on the board at all, which guarantees a true air gap — your signing device has no way to communicate wirelessly, period.

**Other compatible models:** Raspberry Pi 2, 3, 4, and Zero W / WH / 2W all work with SeedSigner. These models do have wireless hardware on the board, but since version 0.4.5 the SeedSigner software disables Wi-Fi and Bluetooth at boot, creating a "software air gap." This is a reasonable option if you already own one of these boards or cannot find a v1.3.

> **Tip:** If you use a wireless-capable Pi and want extra assurance, community members have documented hardware methods to permanently disable the wireless chips. See the [hardware wireless disable guide](https://github.com/DesobedienteTecnologico/rpi_disable_wifi_and_bt_by_hardware) for details.

**A note about the Pi Zero's USB ports:** The Pi Zero has two Micro USB ports. The port nearest the joystick (once the HAT is attached) is **power only**. The other port carries both power and data. For normal SeedSigner use, plug your power source into the **power-only** port.

### 2. Waveshare 1.3" 240x240 LCD HAT

This small display sits on top of the Pi and also provides your controls: a joystick and three buttons. Make sure you get the **240x240 pixel version** specifically — Waveshare sells several display HATs, and other resolutions will not work.

The display typically costs **$15 or less** from most retailers.

> **Warning:** Double-check that the listing says "240x240" before you buy. Other Waveshare LCD HATs look similar but are not compatible.

### 3. Raspberry Pi-Compatible Camera

Most SeedSigner builders choose the **OV5647-based camera module**, which runs about **$10**. This is the same sensor used in the original Raspberry Pi Camera Module v1.

If you are building with a **Pi Zero**, you need the **Zero-compatible ribbon cable** — it is narrower than the standard ribbon cable and has a gold-colored connector. Many camera listings include both cables; if yours does not, order the Zero cable separately.

The camera is also available in a **compact form factor** (a smaller board), which fits neatly into certain enclosure designs. Check the [enclosures page](/hardware-build/enclosures.md) before buying so you pick the right form factor.

## Additional items

You probably already have these around the house:

- **MicroSD card** — Minimum 1 GB capacity. Any brand works. This holds the SeedSigner software image.
- **Micro USB cable** — A standard phone-charging cable.
- **Power source** — A phone charger, laptop USB port, or portable battery pack all work fine.

> **Warning:** Avoid 9V-to-USB adapters. They may not supply enough current to reliably power the camera, which can cause startup failures or erratic behavior.

## Summary table

| Component | Approx. Cost | Notes |
|---|---|---|
| Raspberry Pi Zero v1.3 | ~$15 | No wireless hardware — true air gap. Other Pi models also compatible. |
| Waveshare 1.3" 240x240 LCD HAT | ~$15 | Must be the 240x240 version. Includes joystick and 3 buttons. |
| OV5647 camera module | ~$10 | Get the Zero-compatible ribbon cable if using a Pi Zero. |
| MicroSD card | ~$5 | 1 GB minimum. You likely already have one. |
| Micro USB cable + power source | ~$0–5 | Any standard phone charger or USB port works. |
| **Total** | **~$50** | |

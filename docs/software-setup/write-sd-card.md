# Write the SD card

> Flash the verified SeedSigner image onto a MicroSD card.

## What you need

- A **MicroSD card** — 1 GB minimum capacity. A basic, inexpensive card works fine.
- An **SD card writer** — either a USB adapter or a built-in card slot on your computer.

## Recommended imaging tools

Either of these free, cross-platform tools will get the job done:

- **[Balena Etcher](https://etcher.balena.io/)** — simple interface, hard to make a mistake.
- **[Raspberry Pi Imager](https://www.raspberrypi.com/software/)** — made by the Raspberry Pi Foundation, supports custom images.

Both work on Windows, macOS, and Linux. Pick whichever you prefer.

## Flash the image

1. **Insert your MicroSD card** into your computer using your SD card writer.
2. **Open your imaging tool** (Balena Etcher or Raspberry Pi Imager).
3. **Select the SeedSigner `.img` file** you downloaded and verified in the previous step. If using Raspberry Pi Imager, choose the "Use custom" option to select your own image file.
4. **Select your MicroSD card** as the target drive.
5. **Write the image.** The tool will flash the image and verify the write. This usually takes a minute or two.
6. **Eject the card safely** using your operating system's eject function before removing it.

> **Warning:** Double-check that you selected the correct target drive. The imaging tool will overwrite everything on the selected drive.

## Insert the card into your SeedSigner

Locate the MicroSD card slot on your Raspberry Pi Zero and gently insert the flashed card. The slot is on the underside of the board, near the edge — the card clicks into place.

## A note on removable media and security

After SeedSigner boots, the entire operating system loads into RAM. Once you see the main menu, you can **remove the MicroSD card** from the device.

Why would you do this? With the card removed, there is no persistent storage connected to the device. Nothing can be written or saved — not by the software, and not by any potential exploit. This is one of SeedSigner's strongest security properties.

> **Tip:** Removing the SD card after boot is optional, but it gives you the highest level of assurance that your signing device is truly air-gapped and stateless.

## Next step

Power on your device and follow the [first-run configuration](/software-setup/first-run.md) guide.

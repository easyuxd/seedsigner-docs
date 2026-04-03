# Assembly instructions

> How to assemble a SeedSigner device from individual components — no soldering required.

Everything connects with friction-fit connectors and press-on headers.

<!-- TODO: Add assembly overview photo showing all components laid out before assembly -->

## What you need

Before you start, make sure you have:

- Raspberry Pi Zero (or other compatible Pi)
- Waveshare 1.3" 240x240 LCD HAT
- Camera module with the correct ribbon cable for your Pi
- A flashed MicroSD card (see the [Software Setup guide](/software-setup/download-and-verify.md) for how to prepare this)

## Steps

### 1. Attach the camera ribbon cable

Locate the small camera connector on the Pi Zero — it is a narrow, flat connector near one end of the board. Gently lift the locking tab, slide the ribbon cable in with the contacts facing the board, and press the locking tab back down to secure it.

> **Tip:** The ribbon cable is delicate. Use a light touch when opening the locking tab — it only needs to lift a millimeter or two. If it feels like it is resisting, do not force it.

### 2. Seat the Waveshare LCD HAT

Line up the Waveshare HAT's female header with the GPIO pins on the Pi Zero. Press it down firmly and evenly until the HAT sits flush. The display should be centered over the Pi board.

### 3. Insert the MicroSD card

Slide your flashed MicroSD card into the slot on the underside of the Pi Zero. The card clicks into place.

### 4. Add an enclosure (optional)

If you have a 3D-printed or commercial enclosure, install the assembled unit into it now. See the [enclosures page](/hardware-build/enclosures.md) for available options.

No enclosure is strictly required — SeedSigner runs perfectly fine on an open bench while you get familiar with it.

## That's it

Plug in a Micro USB power source and your SeedSigner device will boot up. Head to [Power on and first boot](/getting-started/first-boot.md) for what to expect on screen. The first boot takes a little longer than usual, so give it a moment.

## Detailed visual guides

The SeedSigner GitHub repository includes detailed assembly guides with photos for specific enclosure designs and component combinations. Check the [SeedSigner enclosures directory](https://github.com/SeedSigner/seedsigner/tree/dev/enclosures) for build documentation that matches your particular setup.

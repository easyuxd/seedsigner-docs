# Common issues

> Symptoms and step-by-step fixes for the most frequently encountered SeedSigner problems.

Work through each suggestion in order — most issues are resolved within the first few steps.

---

## Device won't boot

If your SeedSigner shows no signs of life when you connect power, work through these checks:

1. **Verify your power source.** SeedSigner needs a stable 5V supply with at least 2A of current. Many phone chargers fall short. Use a quality USB-C or Micro-USB power adapter rated for Raspberry Pi.
2. **Check all hardware connections.** Make sure the camera ribbon cable is fully seated in the connector (the plastic latch should be pressed down firmly). Confirm the WaveShare LCD HAT is pushed all the way onto the GPIO header with no bent pins.
3. **Try a different SD card.** Re-flash a fresh SeedSigner image onto a known-good microSD card. Cheap or worn-out cards are a common culprit.
4. **Try a different power cable.** USB cables degrade over time, and some are charge-only with no data lines. Swap in a different cable to rule this out.
5. **Avoid 9V-to-USB adapters.** These battery adapters often cannot supply enough sustained current and may cause intermittent boot failures.

> **Tip:** If you see a brief flash on the screen followed by nothing, the power supply is the most likely problem. Try a Raspberry Pi-specific power adapter.

---

## QR code scanning problems

QR scanning depends on lighting, distance, and camera settings. If scans are failing or taking too long, try these fixes:

1. **Improve lighting.** The camera needs even, adequate light on the QR code. Avoid harsh shadows or direct glare on a phone screen.
2. **Adjust your distance.** Hold the SeedSigner 6 to 12 inches from the QR code. Too close and the camera can't focus; too far and the code is too small.
3. **Clean the camera lens.** A fingerprint or speck of dust on the tiny lens dramatically reduces scan quality. Wipe it gently with a microfiber cloth.
4. **Lower QR code density.** If you're generating QR codes from SeedSigner, navigate to **Settings > Advanced > QR Density** and choose a lower density. Fewer pixels per frame means easier scanning.
5. **Check camera rotation settings.** If the preview image looks rotated, go to **Settings > Advanced > Camera Rotation** and toggle between 0° and 180°.
6. **Run the I/O Test.** Go to **Settings > I/O Test** to confirm the camera is working at all. If you see no image, re-seat the ribbon cable.

### Scanning animated QR codes into Sparrow

When scanning animated (multi-frame) QR codes displayed by Sparrow Wallet:

- Press the joystick **up or down** on SeedSigner to adjust screen brightness. This can help the camera pick up frames more reliably.
- Try **lowering the ambient light** in the room to reduce glare on your computer screen.
- Move the SeedSigner slowly closer or further from the screen until scanning picks up speed.

> **Tip:** Sparrow lets you adjust the animated QR frame rate and density. Slowing down the animation or reducing density on the Sparrow side can help SeedSigner keep up.

---

## Button response issues

If buttons feel unresponsive or register inconsistently:

1. **Run the Hardware I/O Test.** Navigate to **Settings > I/O Test** and press each button. The test screen shows you exactly which inputs are registering.
2. **Clean around the buttons.** Dust or debris can get under the button caps on the WaveShare HAT. Gently blow compressed air around the edges.
3. **Check for physical damage.** Inspect the WaveShare HAT for cracked solder joints or bent components near the buttons.
4. **Try different buttons.** All three keys (A, B, and C) on the WaveShare HAT are identical. If one key responds but another doesn't, the issue is with that specific switch, not the software.

> **Warning:** Do not attempt to disassemble the WaveShare HAT buttons unless you are comfortable with small electronics. You could cause further damage.

---

## Display problems

If the screen is blank, garbled, or showing incorrect colors:

1. **Check the HAT connection.** Remove the WaveShare LCD HAT from the GPIO header and re-seat it firmly. Make sure all pins are aligned and none are bent.
2. **Verify the display type setting.** Go to **Settings > Advanced > Hardware > Display Type** and make sure it matches the exact WaveShare model you have. An incorrect setting can cause a blank or garbled screen.
3. **Run the I/O Test.** If you can navigate the menus at all, run the I/O Test to confirm the display is responding to commands.
4. **Try a different power source.** Insufficient power can cause display flickering or failure to initialize.
5. **Try the color inversion setting.** If colors look inverted (negatives), toggle the color inversion option in the display settings.

---

## Camera shows upside-down image

This is a simple settings mismatch — the camera module can be installed in either orientation.

Go to **Settings > Advanced > Camera Rotation** and switch between **0°** and **180°**. One of the two will match your camera's physical orientation.

> **Tip:** There is no "wrong" way to install the camera ribbon cable orientation-wise. Just match the rotation setting to however your camera is mounted.

# Hardware settings

> Display driver and color settings for your specific hardware.

**Navigation:** Main Menu > Settings > Advanced > Hardware

If your screen looks wrong out of the box, this is the place to fix it.

---

## Settings reference

| Setting | Path | Options | Default |
|---------|------|---------|---------|
| **Display Type** | Hardware | st7789 240x240, st7789 320x240, ili9341 320x240 (beta) | st7789 240x240 |
| **Color Inversion** | Hardware | Enabled, Disabled | Enabled |

---

## Details

### Display type

Select the driver that matches the LCD display in your SeedSigner build. The device needs the correct driver to communicate with the screen — choosing the wrong one will result in a blank or garbled display.

| Driver | Resolution | Notes |
|--------|-----------|-------|
| **st7789 240x240** | 240 x 240 | Default. Used by the most common SeedSigner display modules. |
| **st7789 320x240** | 320 x 240 | For larger st7789-based displays. |
| **ili9341 320x240** | 320 x 240 | Beta support. Use only if your display uses the ILI9341 controller. |

> **Warning:** You must select the driver that matches your actual hardware. An incorrect selection will cause the display to malfunction. If you are unsure which display you have, check the markings on the back of the LCD board or refer to the product listing from your supplier.

> **Tip:** If you just swapped to a new display and the screen is blank, reflash the SD card with the correct display driver selected.

### Color inversion

Controls whether display colors are inverted. The default (Enabled) produces correct colors on most common SeedSigner display modules.

If your display shows inverted or "negative" colors — for example, white text on areas that should be dark, or a generally washed-out appearance — try toggling this setting.

---

## Diagnosing display and button issues

If your display or buttons are not behaving as expected, use the **I/O Test** found under **Settings > I/O Test** (see [Basic Settings](/configuration/basic.md)). The test walks you through each hardware component so you can quickly identify what is and is not working.

Common scenarios where the I/O test helps:

- Display shows content but colors look wrong (check Color Inversion and Display Type)
- A button press is not registering (could be a wiring issue or a stuck button)
- Camera preview is blank or distorted (may need a different camera ribbon cable or rotation setting in [Advanced Settings](/configuration/advanced.md))

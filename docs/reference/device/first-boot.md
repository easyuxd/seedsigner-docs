# First boot

> Step-by-step instructions for powering on your SeedSigner device and reaching the main menu.

Your SeedSigner device is assembled, the software is flashed to your microSD card, and you are ready to go.

## Connect power

Plug a micro USB cable into the **power-only port** on your SeedSigner. This is the port **nearest to the joystick**. Connect the other end to any USB power source — a phone charger, power bank, or computer USB port all work fine.

> **Warning:** Use the correct port. The port farther from the joystick is for data and will not reliably power the device on its own.

## Wait for boot: the screen stays blank for a while

After you connect power, **expect the screen to stay completely blank for around 45 seconds** on a Pi Zero v1.3 before the SeedSigner splash screen appears (the faster Pi Zero 2 W boots in roughly half that). This is normal: the entire operating system is loading from the SD card into RAM.

Don't unplug it, don't press anything — just wait for the splash screen.

> **Tip:** A blank screen for the first minute does **not** mean the device is dead or mis-assembled. Only start troubleshooting if nothing has appeared after about 90 seconds — then see [Common issues](/help/common-issues.md#device-wont-boot).

## Dismiss the SD card message

Once the boot process finishes, a message appears on screen telling you that you can safely remove the microSD card. Press **any button** (A, B, or C) to dismiss this message and continue.

## You're at the main menu

After dismissing the message, you land on the main menu. From here you can create seeds, scan QR codes, access tools, and configure settings.

![SeedSigner main menu showing Seeds, Scan, Tools, and Settings options](../../images/MainMenuView.png)

## Remove the SD card for maximum security

SeedSigner's operating system loads entirely into RAM during boot. Once the SD card message appears, the card is no longer needed. You can physically eject it and set it aside.

Why do this? With the microSD card removed, there is **no writable storage** connected to the device. This makes it impossible for any private data (seed phrases, private keys, or anything else) to be saved to disk. Your secrets exist only in volatile memory and vanish the moment you unplug the device.

> **Tip:** Removing the SD card is optional but recommended whenever you are working with real funds.

## Next steps

Now that your device is running, learn how to move around the interface in [Navigation basics](/reference/device/navigation.md).

> **Tip:** If the screen stays blank or the device does not boot, see [Common issues](/help/common-issues.md#device-wont-boot).

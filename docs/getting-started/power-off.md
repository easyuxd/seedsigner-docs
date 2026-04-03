# Power off and restart

> How to safely shut down or restart your SeedSigner device.

SeedSigner gives you two ways to power off and a clean way to restart. Because the device stores nothing permanently by default, both methods are safe.

## Power off — Method 1: Use the menu

This is the recommended way to shut down.

1. From the main menu, use the joystick to highlight the **power icon** in the top-right corner.
2. Press any key (A, B, or C) to open the power options menu.

![Power options menu showing Power Off and Restart choices](/images/PowerOptionsView.png)

3. Select **Power Off**.

![Power off confirmation screen](/images/PowerOffView.png)

4. Confirm when prompted. The device shuts down.

## Power off — Method 2: Unplug the cable

You can simply disconnect the micro USB power cable at any time. SeedSigner does not store private data to disk, so there is nothing to corrupt. All temporary data in RAM — loaded seeds, in-progress transactions, and anything else — is erased the instant power is removed.

> **Tip:** Unplugging is perfectly safe. There is no "improper shutdown" risk with SeedSigner because the operating system runs entirely from RAM.

## Restart the device

If you want to clear temporary data without fully powering down and reconnecting the cable:

1. From the main menu, highlight the **power icon** in the top-right corner and press any key.
2. Select **Restart** from the power options menu.

![Restart confirmation screen](/images/RestartView.png)

3. The device reboots automatically. You will see the splash screen and the SD card message again, just like a fresh boot.

> **Warning:** Restarting clears all temporary data from memory. Any loaded seed phrases, partially signed transactions, or other session data will be gone. Make sure you have recorded anything you need before restarting.

If you have enabled **persistent settings** in the Settings menu, your configuration preferences (display brightness, network selection, etc.) are saved to the microSD card and will survive a restart. Your seed phrases and private keys are never persisted — those are always cleared.

## Next step

Now that you know how to control your device, head to [Create your first seed](/using-seedsigner/create-seed.md) to start using SeedSigner for real.

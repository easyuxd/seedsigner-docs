# Discard a loaded seed

> Remove a seed from SeedSigner's memory after you are done using it.

When you are finished signing or managing keys, discard the seed from memory. This is a security best practice — do not leave seeds loaded longer than necessary.

## Step-by-step

1. Navigate to **Seeds** → select the loaded seed → **Discard Seed**.

   ![Discard option](/images/DiscardSeedSelectView.png)

2. Confirm by selecting **Discard**.

   ![Confirm discard](/images/DiscardSeedMainMenuView.png)

3. You are returned to the main menu with no seed loaded.

   ![Main menu](/images/MainMenuView.png)

## What happens

Discarding a seed completely erases it from volatile RAM. No trace of the seed remains on the device. This is functionally identical to unplugging SeedSigner, except the device stays powered on and ready for other operations.

> **Tip:** If you are switching between different seeds (for example, signing a multi-sig transaction with multiple keys), discard the current seed before loading the next one.

## Alternative: just unplug

Because SeedSigner is stateless, you can also simply unplug the power cable at any time. All data in RAM — including any loaded seeds — is permanently erased when power is removed.

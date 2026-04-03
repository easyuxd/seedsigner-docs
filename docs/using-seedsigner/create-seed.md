# Create a new seed

> Generate a new BIP-39 seed phrase using camera entropy, dice rolls, or manual word selection.

SeedSigner offers three ways to create a brand-new seed phrase. Each method captures physical entropy (randomness from the real world) so that your private key is unpredictable and secure.

## Choose your method

| Method | How it works | Rolls / steps | Best for |
|--------|-------------|---------------|----------|
| **Camera** | Captures randomness from a photograph | 1 photo | Quick seed creation |
| **Dice** | Converts physical dice rolls into a seed | 50 (12-word) or 99 (24-word) | Maximum provable randomness |
| **Calculate final word** | You supply 11 or 23 words; SeedSigner computes the checksum word | Manual entry + entropy | Users who select their own words |

> **Tip:** A 24-word seed provides more entropy than a 12-word seed. For long-term cold storage, 24 words is recommended. For multi-signature setups, 12-word seeds per key can be sufficient.

---

## Method 1: Camera-based seed generation

This method uses environmental entropy captured by the camera — pixel data, preview frames, the Pi's serial number, and the elapsed uptime in milliseconds are all mixed together.

1. From the main menu, select **Tools**.

   ![Main menu with Tools option highlighted](/images/ToolsOptionSelectView.png)

2. Select **New Seed** (camera icon).

   ![Tools menu showing New Seed options for camera and dice](/images/ToolsMenuView.png)

3. Point the camera at a random, moving scene (trees, clouds, traffic). Press any key to capture.

   ![Camera viewfinder capturing environmental entropy](/images/SeedCameraEntropyView.png)

4. Review the captured image. Push the joystick **left** to retake, or **right** to accept.

   ![Entropy preview](/images/SeedEntropyPreviewView.png)

5. Choose **12 words** or **24 words**.

   ![Seed length selection showing 12-word and 24-word options](/images/SeedMnemonicLengthView.png)

6. Read the security warning and press **I Understand**.

   ![Security warning](/images/SeedWarningView.png)

7. **Write down every word** in exact order. Words display four at a time. Double-check each one.

   ![Generated seed words displayed four at a time](/images/SeedMnemonicEntryView.png)

8. Complete the **backup verification** quiz. SeedSigner asks you to confirm specific words to prove your written backup is correct.

   ![Backup verification quiz prompting for a specific seed word](/images/SeedBackupTestView.png)

> **Warning:** If you write even one word incorrectly, you could permanently lose access to your Bitcoin. Never skip the verification step. If you see an error, see [Error messages](/troubleshooting/error-messages.md) for help.

---

## Method 2: Dice-based seed generation

Physical dice produce true randomness that cannot be influenced by software bugs or hardware backdoors. This is the most trust-minimized method.

1. From the main menu, select **Tools**.
2. Select **New Seed** (dice icon).

   ![Dice method](/images/SeedGenerateDiceMethodView.png)

3. Choose your seed length:
   - **12 words** = 50 dice rolls
   - **24 words** = 99 dice rolls

   ![Dice seed length](/images/SeedMnemonicLengthDiceView.png)

4. Roll a standard six-sided die. On the screen, press the **joystick** in the direction of the number you rolled (1--6). Repeat for every roll.

   ![Dice entry](/images/ToolsDiceEntropyEntryView.png)

5. A progress bar shows how many rolls remain.

   ![Dice progress](/images/ToolsDiceEntropyProgressView.png)

6. Read the security warning and press **I Understand**.
7. Write down all seed words and complete the backup verification.

> **Tip:** Use a casino-grade die for the best randomness. Roll on a flat, hard surface.

---

## Method 3: Calculate the 12th or 24th word

If you want to choose your own words from the BIP-39 word list, this method lets you enter 11 or 23 words and then computes a valid final checksum word.

1. From the main menu, select **Tools** → **Calc 12th/24th word**.

   ![Calc method](/images/SeedGenerateCalcMethodView.png)

2. Choose **12 words** or **24 words**.

   ![Calc seed length](/images/SeedMnemonicLengthCalcView.png)

3. Enter each word using the on-screen keyboard:
   - **Key A** — move up in the suggestion list
   - **Key C** — move down in the suggestion list
   - **Key B** — select the highlighted word
   - Type the first 2--3 letters and pick from suggestions for speed.

   ![Word entry](/images/WordEntry.png)

4. After entering all words, choose how to generate entropy for the final word:

   ![Finalize prompt](/images/ToolsCalcFinalWordFinalizePromptView.png)

   - **Coin flips** — Flip a physical coin 7 times; enter heads (1) or tails (0) for each.
   - **Word selection** — Pick any word from the BIP-39 list as your entropy source.
   - **Zeros** — Uses a 7-bit string of zeros (simplest, still valid).

5. SeedSigner displays the calculated final word along with the derivation details.

   ![Final word display](/images/ToolsCalcFinalWordShowFinalWordView.png)

6. Your complete seed phrase is now ready for backup and use.

> **Technical note:** The final word in any BIP-39 seed phrase contains both entropy bits and a checksum. The checksum detects transcription errors and proves the phrase is mathematically valid.

---

## What to do next

After creating your seed, SeedSigner loads it into memory. You can now:

- [Export your public key (xpub)](/using-seedsigner/export-xpub.md) to set up a watch-only wallet
- [Back up your seed as a SeedQR](/using-seedsigner/seedqr-backup.md) for fast future loading
- [Sign a transaction](/using-seedsigner/sign-transaction.md) if your wallet is already configured

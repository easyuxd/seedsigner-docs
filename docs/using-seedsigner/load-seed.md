# Load an existing seed

> Enter an existing seed phrase into SeedSigner by typing words or scanning a SeedQR.

If you already have a BIP-39 seed phrase, you can load it into SeedSigner either by typing the words manually or by scanning a SeedQR code.

---

## Option 1: Manual word entry

Use this when you have your seed words written on paper or stamped in metal.

1. From the main menu, select **Seeds** → **Load a Seed**.

   ![Seeds menu](/images/SeedsOptionSelectView.png)

   ![Load a seed](/images/LoadASeedMainOptionSelectView.png)

2. Choose **Enter 12-word seed** or **Enter 24-word seed**.

   ![Seed length](/images/LoadASeedMainMenuView.png)

3. Type each word using the on-screen keyboard:
   - Use the joystick to move between letters.
   - **Key A** — move up in the suggestion list.
   - **Key C** — move down in the suggestion list.
   - **Key B** — select the highlighted suggestion.

   ![Word entry](/images/SeedWordEnterView.png)

> **Tip:** You only need to type the first 2--3 letters of each word. The suggestion list narrows quickly, making entry much faster.

4. After entering all words, review the **seed fingerprint** on the Finalize Seed screen. This short identifier is unique to your seed and helps you confirm you entered the right one.

   ![Finalize seed](/images/SeedFinalizeView.png)

5. Choose your next step:
   - **Done** — Load the seed as-is.
   - **BIP-39 Passphrase** — Add an optional passphrase for additional security (see below).

---

## Option 2: Scan a SeedQR

Use this when you have a SeedQR code — a compact QR that encodes your entire seed phrase.

1. From the main menu, select **Scan**.

   ![Main menu scan](/images/MainMenuView.png)

2. Point the camera at your SeedQR code. Hold the device 6--12 inches away and keep it steady.

   ![Scanning](/images/SeedQRScan.png)

3. SeedSigner automatically detects and decodes the QR. When successful, you see the Finalize Seed screen with your seed fingerprint.

   ![Finalize](/images/SeedFinalizeView.png)

4. Select **Done** to load the seed, or add a BIP-39 passphrase first.

> **Warning:** If you see "Unknown QR Type," the QR code is not a valid SeedQR format. Verify you are scanning a properly formatted SeedQR and not a regular QR code. See [Error messages](/troubleshooting/error-messages.md#unknown-qr-type) for details.

---

## Adding a BIP-39 passphrase

A BIP-39 passphrase acts as an extra word appended to your seed phrase. It transforms the underlying private key into a completely different key. This means:

- The same 12 or 24 words **with** a passphrase produce a **different wallet** than without one.
- If someone discovers your seed words but not the passphrase, they cannot access the passphrase-protected wallet.
- If you forget the passphrase, the funds in that wallet are permanently inaccessible.

To add a passphrase, select **BIP-39 Passphrase** on the Finalize Seed screen and enter your passphrase using the on-screen keyboard.

> **Warning:** A passphrase is case-sensitive and space-sensitive. "MyPass" and "mypass" produce completely different wallets. Write it down and store it separately from your seed words.

---

## What to do next

With your seed loaded, you can:

- [Export your public key (xpub)](/using-seedsigner/export-xpub.md)
- [Sign a transaction](/using-seedsigner/sign-transaction.md)
- [Explore your addresses](/using-seedsigner/addresses.md)
- [View your seed words](/using-seedsigner/view-seeds.md) to verify your backup

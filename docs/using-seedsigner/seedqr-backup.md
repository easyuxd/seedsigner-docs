# Back up with SeedQR

> Encode your seed phrase as a compact QR code for fast future loading.

A SeedQR encodes your entire seed phrase into a compact QR code. Instead of typing 12 or 24 words every time you need to load a seed, you simply hold the SeedQR in front of the camera and your seed is loaded in seconds.

## Before you begin

You need a seed [loaded into SeedSigner](/using-seedsigner/load-seed.md).

## Create a SeedQR backup

1. From the loaded seed menu, select **Backup Seed** → **Export as SeedQR**.

   ![Backup seed](/images/BackupSeedSelectView.png)

   ![Export as SeedQR](/images/ExportAsSeedQRSelectView.png)

2. Choose a format:
   - **Standard (25x25)** — larger QR, easier to hand-draw and scan.
   - **Compact (21x21)** — smaller QR, requires more precise transcription.

   ![Format selection](/images/SeedTranscribeSeedQRFormatView.png)

3. Read the security warning and confirm. The QR contains your complete private key.

   ![SeedQR warning](/images/SeedTranscribeSeedQRWarningView.png)

4. SeedSigner displays the full QR code. Select **Begin** to start the section-by-section transcription view.

   ![Full QR](/images/SeedTranscribeSeedQRWholeQRView_12_Standard.png)

5. Use the joystick to navigate through zoomed sections of the QR. Carefully transcribe each section onto paper, a metal plate, or another durable medium.

   ![Zoomed view](/images/SeedTranscribeSeedQRZoomedInView_12_Standard.png)

6. When finished, you have two options:

   ![Confirm prompt](/images/SeedTranscribeSeedQRConfirmQRPromptView.png)

   - **Confirm SeedQR** — the camera opens so you can scan your hand-drawn QR to verify it reads correctly.
   - **Done** — skip verification and return to the seed menu.

> **Tip:** Always choose **Confirm SeedQR** and scan your transcription. A single misplaced dot can make the QR unreadable.

## Verification results

**Success** — Your transcription is accurate and will scan correctly in the future.

![Verification success](/images/SeedTranscribeSeedQRConfirmSuccessView.png)

**Failure** — The scanned QR does not match. Re-examine your transcription for errors and try again.

![Verification failure](/images/SeedTranscribeSeedQRConfirmWrongSeedView.png)

## Printable templates

The SeedSigner GitHub repo includes printable templates for documenting seed phrases and SeedQRs:

[https://github.com/SeedSigner/seedsigner/tree/main/docs](https://github.com/SeedSigner/seedsigner/tree/main/docs)

## Security considerations

- A SeedQR is **equivalent to your written seed backup**. Anyone who can scan it can access your funds.
- Store SeedQRs with the same care as written seed words: in a fireproof safe, safety deposit box, or other secure location.
- Never scan a SeedQR with a phone, computer webcam, or any device that connects to the internet. Only scan it with SeedSigner.
- Consider stamping the QR onto metal for fire resistance and long-term durability.

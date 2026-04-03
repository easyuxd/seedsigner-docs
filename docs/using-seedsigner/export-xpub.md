# Export a public key (xpub)

> Share your extended public key with your coordinator wallet so it can generate addresses and track your balance — without exposing your private key.

You export the xpub once, scan it into your coordinator, and from that point forward you can receive Bitcoin without powering on SeedSigner.

## Before you begin

- You need a seed [loaded into SeedSigner](/using-seedsigner/load-seed.md).
- Have your coordinator wallet software open and ready to scan (for example, Sparrow Wallet).

## Step-by-step

1. From the loaded seed's menu, select **Export Xpub**.

   ![Seed menu](/images/SeedMenuView.png)

2. Choose the **signature type**:
   - **Single Sig** — for a standard personal wallet controlled by one key.
   - **Multisig** — for a multi-signature wallet requiring multiple keys.

   ![Signature type](/images/SeedExportXpubSigTypeView.png)

3. Choose the **script type** (address format):

   | Script type | Format | Recommended for |
   |-------------|--------|-----------------|
   | Native SegWit | bech32 (bc1q...) | Lowest fees, widest modern support |
   | Nested SegWit | P2SH (3...) | Compatibility with older wallets |
   | Taproot | bech32m (bc1p...) | Advanced privacy and scripting |

   ![Script type](/images/SeedExportXpubScriptTypeView.png)

4. Select your **coordinator wallet software** from the list (Sparrow, BlueWallet, Specter, etc.).

   ![Coordinator selection](/images/SeedExportXpubCoordinatorView.png)

5. Read the **privacy warning** and press **I Understand**.

   ![Privacy warning](/images/SeedExportXpubWarningView.png)

6. Review the xpub details, then select **Export Xpub** to display the QR code.

   ![Xpub details](/images/SeedExportXpubDetailsView.png)

7. Scan the QR code with your coordinator's camera (for example, in Sparrow: File → New Wallet → Airgapped Hardware Wallet → SeedSigner → Scan).

   ![Xpub QR code](/images/SeedExportXpubQRView.png)

> **Warning:** Your xpub reveals every address and the full transaction history of your wallet. Treat it as private information. Never post it publicly or share it with anyone you do not trust.

## What happens next

After your coordinator imports the xpub, it builds a **watch-only wallet**. You can:

- Generate receiving addresses to accept payments.
- View your balance and transaction history.
- Prepare unsigned transactions (PSBTs) for SeedSigner to sign later.

None of this requires your private key. SeedSigner only needs to come out of storage when you want to **send** Bitcoin.

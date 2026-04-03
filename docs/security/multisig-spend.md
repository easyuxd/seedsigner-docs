# Spend from a multi-signature wallet

> Sign and broadcast a transaction from a multi-sig wallet by collecting signatures from multiple keys.

Sending Bitcoin from a multi-sig wallet works similarly to single-sig, but you need to collect enough signatures to meet the quorum. For a 2-of-3 wallet, that means signing with any 2 of your 3 keys.

## Step 1: Create the transaction in Sparrow

1. Open your multi-sig wallet in Sparrow.
2. Go to the **Send** tab.
3. Enter the destination address, the amount, and a label for your records.
4. Click **Create Transaction**.
5. Review the transaction details — inputs, outputs, amounts, and fees.
6. Click **Finalize Transaction for Signing**.

## Step 2: Sign with the first key

**In Sparrow:**

1. Click **Show QR** to display the animated PSBT (partially signed Bitcoin transaction) as a series of QR codes.

**On SeedSigner:**

1. Load the first seed you want to sign with.
2. From the main menu, select **Scan**.
3. Point the SeedSigner camera at the animated QR code on your computer screen. The device will read multiple frames automatically.

**Review the transaction on SeedSigner:**

SeedSigner displays the transaction details for your review. Check each screen carefully:

- **PSBT overview** — the number of inputs and outputs
- **Amounts** — how much is being sent
- **Recipients** — the destination address(es)
- **Change** — any amount returning to your wallet
- **Fee** — the mining fee

If everything looks correct, approve the PSBT. SeedSigner generates a signed QR code.

**Scan the signature back into Sparrow:**

1. In Sparrow, click **Scan QR**.
2. Hold the SeedSigner screen in front of your webcam so Sparrow can read the signed QR code.

The first cosigner's signature is now recorded.

## Step 3: Sign with the second key

Repeat the same process with a different seed:

1. In Sparrow, click **Show QR** again to display the updated PSBT.
2. On SeedSigner, load the second seed and scan the QR from your screen.
3. Review the transaction details on SeedSigner and approve.
4. Scan the resulting signed QR back into Sparrow.

After the second signature is recorded, Sparrow will show that the quorum has been met.

## Step 4: Broadcast the transaction

With 2 of 3 signatures collected, click **Broadcast Transaction** in Sparrow. Your transaction is submitted to the Bitcoin network.

> **Tip:** You can sign with any 2 of your 3 keys. It does not matter which 2 you choose — the result is the same.

> **Warning:** You must meet the quorum threshold before broadcasting. For a 2-of-3 wallet, a transaction signed by only 1 key cannot be broadcast. Sparrow will not allow it.

## Summary

| Step | Where | Action |
|------|-------|--------|
| Create transaction | Sparrow | Enter address, amount, finalize |
| First signature | SeedSigner → Sparrow | Scan PSBT, review, approve, scan back |
| Second signature | SeedSigner → Sparrow | Repeat with a different seed |
| Broadcast | Sparrow | Send to the Bitcoin network |

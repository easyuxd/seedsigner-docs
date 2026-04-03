# Back up the wallet descriptor

> Why the wallet descriptor is critical for multi-sig recovery and how to export and store it.

## What is a wallet descriptor?

A wallet descriptor is a small file that contains all the information your coordinator software needs to reconstruct your multi-sig wallet. Specifically, it includes:

- The extended public keys (xpubs) for every cosigner
- The rules that define how those keys combine (for example, 2-of-3)
- The derivation paths used for each key

Think of it as the blueprint for your wallet. Your seed phrases are the raw materials, and the descriptor is the architectural plan that tells software how to assemble them.

## Why you absolutely must back this up

In a single-sig wallet, your seed phrase is all you need to recover your funds. Multi-sig is different.

If you lose 1 of your 3 seeds **and** you do not have the wallet descriptor, your funds are **permanently lost**. Even though you still have 2 valid keys — enough to sign — no software can reconstruct the wallet without knowing how all three keys were originally combined.

> **Warning:** Back up your wallet descriptor before depositing any funds into your multi-sig wallet. This is not optional.

## What the descriptor reveals (and what it does not)

The wallet descriptor is **private but not secret**:

- **It can reveal:** your wallet addresses and transaction history. Anyone who obtains it can see your balances and past activity.
- **It cannot:** move your funds. The descriptor contains only public keys, not private keys. No one can spend your Bitcoin using the descriptor alone.

Treat it with care — you would not want your financial history exposed — but understand that its compromise does not put your funds at direct risk.

## How to export from Sparrow

### As a QR code

1. In Sparrow, go to **File → Export Wallet**.
2. Scroll down to the **Specter Desktop** format.
3. Click **Show** to display the wallet descriptor as a QR code.
4. You can photograph this QR code for backup, or scan it directly with SeedSigner.

### As a file

1. In Sparrow, go to **File → Export Wallet**.
2. Scroll down to the **Specter Desktop** format.
3. Click **Export File** to save a `.json` file to your computer.

## How to store your descriptor backup

Because the descriptor does not contain private keys, you have more flexibility in how you store it:

- **Printed copies** — print the QR code and/or the text content. Store alongside (or near) your seed backups.
- **Digital copies** — save the exported `.json` file to a USB drive or other offline storage.
- **Multiple locations** — consider keeping a copy with each seed backup location, so that any 2 of your 3 storage sites have everything needed for recovery.

> **Tip:** A good practice is to store a copy of the wallet descriptor at each location where you keep a seed backup. That way, if you can access any 2 of your 3 locations, you have both the required seeds and the descriptor.

## Verifying addresses with SeedSigner

SeedSigner can scan the wallet descriptor QR code and use it to verify that receive and change addresses actually belong to your multi-sig wallet. This is a valuable security check:

1. In SeedSigner, scan the wallet descriptor QR code.
2. SeedSigner uses the descriptor to independently derive wallet addresses.
3. Compare these addresses to what Sparrow displays.

If they match, you have confirmation that your wallet is set up correctly and that Sparrow is showing you legitimate addresses.

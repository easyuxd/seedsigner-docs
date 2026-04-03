# What is SeedSigner?

SeedSigner is a do-it-yourself Bitcoin signing device. You assemble it from three inexpensive, general-purpose components, flash an open-source operating system onto an SD card, and you have a fully functional tool for generating seeds, exporting public keys, and signing transactions — all completely air-gapped.

## Core design principles

### Physically isolated

SeedSigner is built on the Raspberry Pi Zero v1.3, a board that **has no Wi-Fi or Bluetooth hardware**. It cannot connect to a network even if compromised software tried to make it do so. The only way data moves in or out is through the camera (input) and the screen (output), using QR codes.

### Stateless

SeedSigner does not store your private keys. When you load a seed, it lives in volatile RAM. The moment you unplug the device, everything is erased. There is no secure element, no encrypted storage, and no flash memory holding secrets. This is intentional — if the device cannot remember your keys, it cannot leak them.

### Affordable and discreet

The bill of materials is roughly $50. All components are generic electronics available from any Raspberry Pi retailer. Nothing about the parts signals "Bitcoin" to a merchant, a shipping carrier, or anyone who might see the package.

### Fully open source

The software is written in Python and published under the MIT license. Anyone can read, audit, and build from source. The hardware is commodity Raspberry Pi — no proprietary chips or black-box firmware controlling key operations.

## What can it do?

| Task | Description |
|------|-------------|
| **Generate a seed** | Create a new BIP-39 seed phrase from camera entropy, dice rolls, or manual word selection |
| **Load a seed** | Enter an existing seed by typing words or scanning a SeedQR |
| **Export an xpub** | Derive and display an extended public key so your coordinator can build a watch-only wallet |
| **Sign a PSBT** | Scan an unsigned transaction, review it on screen, and produce a signed QR |
| **Create a SeedQR** | Encode your seed phrase into a compact QR code for fast future loading |
| **Explore addresses** | Browse receiving and change addresses derived from a loaded seed |
| **Calculate the final word** | Enter 11 or 23 words and compute the valid checksum word |

## How SeedSigner fits into your setup

SeedSigner is the **signer** in a signer-plus-coordinator architecture. It holds private keys temporarily and produces signatures. It does not connect to the Bitcoin network.

You pair it with a **coordinator** — a wallet application running on a networked computer or phone. The coordinator builds transactions, manages addresses, and talks to the Bitcoin network. Popular coordinators include:

- [Sparrow Wallet](https://sparrowwallet.com) (desktop)
- [Specter Desktop](https://specter.solutions) (desktop, requires a node)
- [BlueWallet](https://bluewallet.io) (mobile)
- [Nunchuk](https://nunchuk.io) (mobile and desktop)
- [Keeper](https://bitcoinkeeper.app) (mobile)

## Who is SeedSigner for?

- **New Bitcoiners** who want affordable self-custody with solid security defaults.
- **Privacy-conscious users** who prefer hardware that cannot phone home.
- **Multi-sig users** who need multiple signers without buying multiple expensive hardware wallets.
- **Developers and tinkerers** who want to audit, modify, or extend a signing device.
- **Bitcoiners in restrictive jurisdictions** who need discreet, unrecognizable hardware.

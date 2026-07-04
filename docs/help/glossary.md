# Glossary

> Key terms used throughout this documentation, listed alphabetically.

| Term | Definition |
|------|-----------|
| **Air gap** | Physical isolation of a device from all networks (Wi-Fi, Bluetooth, USB data). SeedSigner achieves this by using hardware that lacks wireless capabilities and communicating only through QR codes. |
| **BIP** | Bitcoin Improvement Proposal. A design document for introducing features or standards to Bitcoin. Examples: BIP-39 (seed phrases), BIP-174 (PSBTs). |
| **BIP-39** | The standard that defines mnemonic seed phrases (12 or 24 words) for generating Bitcoin private keys. |
| **BIP-39 passphrase** | An optional extra word or phrase added to a BIP-39 seed. It produces a completely different private key and wallet from the same seed words. Sometimes called the "25th word." |
| **BIP-85** | A standard for deriving child seed phrases deterministically from a parent seed. Useful for creating separate wallets that can all be recovered from a single master seed. |
| **Change address** | An address in your wallet that receives the leftover funds from a transaction. Managed automatically by your coordinator wallet. |
| **Checksum** | The error-detection component encoded in the final word of a BIP-39 seed phrase. It helps catch transcription mistakes. |
| **Compact SeedQR** | A 21x21 version of SeedQR that uses less space but requires more precise transcription than the standard 25x25 format. |
| **Coordinator** | Wallet software (such as Sparrow, Specter, or BlueWallet) that runs on a networked device. It manages addresses, builds unsigned transactions, and broadcasts signed transactions. It does not hold private keys when used with SeedSigner. |
| **Cosigner** | One of the key holders in a multi-signature wallet. A 2-of-3 wallet has three cosigners, any two of whom can authorize a spend. |
| **Entropy** | Randomness used to generate a private key. Sources include camera images, dice rolls, and coin flips. Higher entropy means a more secure key. |
| **Extended public key (xpub)** | A public key that can derive a sequence of child public keys (and thus addresses). Exported from SeedSigner to your coordinator so it can generate receiving addresses without the private key. |
| **GPIO** | General-Purpose Input/Output pins on the Raspberry Pi board. The Waveshare LCD HAT connects via these pins. |
| **Mainnet** | The real Bitcoin network where transactions involve actual value. Contrast with testnet. |
| **Multi-signature (multi-sig)** | A wallet that requires signatures from multiple private keys (e.g., 2 of 3) to authorize a transaction. Provides fault tolerance against key loss or disclosure. |
| **Native SegWit** | A Bitcoin address format (bech32, starting with bc1q...) that offers the lowest transaction fees. Recommended default. |
| **Nested SegWit** | A Bitcoin address format (P2SH, starting with 3...) that is compatible with older wallets and services. |
| **PSBT** | Partially Signed Bitcoin Transaction (BIP-174). A standardized format for an unsigned or partially signed transaction that can be passed between devices for signing. |
| **Quorum** | The set of cosigners in a multi-signature wallet, along with the signing threshold. "2-of-3" means 3 total keys with 2 required to sign. |
| **Raspberry Pi Zero** | A small, inexpensive single-board computer. Version 1.3 lacks Wi-Fi and Bluetooth, making it ideal for an air-gapped signer. |
| **Receiving address** | A Bitcoin address you share with others to accept payments. Best practice: use a new one for each transaction. |
| **Script type** | The type of Bitcoin address format: Native SegWit, Nested SegWit, or Taproot. Determines address prefix and fee structure. |
| **SD card** | The MicroSD memory card that holds the SeedSigner operating system image. After boot, the OS loads into RAM and the card can optionally be removed. |
| **Seed phrase** | A sequence of 12 or 24 words (from the BIP-39 word list) that encodes a Bitcoin private key. Also called a mnemonic. |
| **SeedQR** | A compact QR code format that encodes a BIP-39 seed phrase. Used for fast seed loading into SeedSigner via the camera. |
| **Signer** | A device (like SeedSigner) that holds private keys and produces cryptographic signatures for transactions. It does not connect to the Bitcoin network. |
| **Single-signature (single-sig)** | A wallet controlled by a single private key. Simpler than multi-sig but has a single point of failure. |
| **Stateless** | A device that does not retain data after power is removed. SeedSigner stores nothing to disk — all key material exists only in volatile RAM. |
| **Taproot** | A Bitcoin address format (bech32m, starting with bc1p...) that offers advanced privacy and smart-contract features. |
| **Testnet** | A separate Bitcoin network used for development and testing. Testnet coins have no value. |
| **Wallet descriptor** | A file or data structure that defines how a multi-signature wallet is constructed: which public keys, in what order, and what signing threshold. Essential backup for multi-sig recovery. |
| **Waveshare LCD HAT** | A 1.3-inch, 240x240 pixel display module with joystick and buttons that connects to the Raspberry Pi's GPIO pins. Serves as SeedSigner's screen and controls. |

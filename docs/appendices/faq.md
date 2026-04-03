# Frequently asked questions

> Quick answers to common questions about SeedSigner, security, seeds, and compatibility.

## General

### What is SeedSigner?

SeedSigner is an open-source, air-gapped Bitcoin signing device. You build it from a Raspberry Pi Zero, a camera, and an LCD display. It generates seed phrases, exports public keys, and signs transactions — all without connecting to any network.

### How much does it cost to build?

Approximately $50 for all components. The Raspberry Pi Zero is around $15, the Waveshare LCD HAT is around $15, the camera is around $10, and you need a MicroSD card and USB cable (most people already have these).

### Is SeedSigner a wallet?

No. SeedSigner is a **signer** — it holds private keys temporarily and produces signatures. You pair it with a **coordinator wallet** (like Sparrow, BlueWallet, or Nunchuk) that runs on a networked computer or phone. The coordinator handles addresses, balances, and broadcasting transactions.

### Does SeedSigner store my private keys?

No. SeedSigner is stateless. Your seed exists only in volatile RAM while the device is powered on. When you unplug it, everything is erased. You must have a separate backup (written words, SeedQR, metal plate) to reload your seed.

---

## Security

### How is SeedSigner air-gapped?

The Raspberry Pi Zero v1.3 has no Wi-Fi or Bluetooth hardware. It physically cannot connect to any network. Data moves in and out only through the camera (scanning QR codes) and the screen (displaying QR codes).

### Can I use a Raspberry Pi with Wi-Fi?

Yes. SeedSigner supports Pi 2, 3, 4, and Zero W/WH/2W. Since version 0.4.5, the software disables wireless modules, creating a "software air gap." For maximum assurance, use a Pi Zero v1.3 (hardware air gap) or physically disable the wireless chip on other models.

### Should I remove the SD card after booting?

You can, and it adds an extra layer of security. After SeedSigner boots, the operating system runs entirely from RAM. Removing the SD card ensures nothing can be written to persistent storage. This is optional but recommended for sensitive operations.

### Is the SeedSigner software safe to use?

SeedSigner is fully open-source and community-audited. However, **you are your own software validation mechanism.** Always download releases from the official GitHub repository and verify the PGP signature and SHA256 hash before flashing. See [Download and Verify](/software-setup/download-and-verify.md).

### What happens if someone steals my SeedSigner?

If the device is powered off, there is nothing to steal — no keys are stored. A thief gets a Raspberry Pi with generic software on the SD card. Your seed backups (written words, SeedQR) are what you need to protect.

---

## Seeds and keys

### 12-word or 24-word seed — which should I use?

A 24-word seed has more entropy and is recommended for single-signature wallets. For multi-signature wallets, 12-word seeds per cosigner can be sufficient because the overall security comes from the combination of multiple keys. 12-word seeds are also easier to manage as SeedQR codes.

### What is a BIP-39 passphrase?

An optional extra word that transforms your seed into a completely different private key. The same 12 or 24 words with a passphrase produce a separate wallet from the same words without one. This protects against seed disclosure — but if you forget the passphrase, you lose access to that wallet.

### What is a SeedQR?

A compact QR code that encodes your entire seed phrase. Instead of typing 12 or 24 words, you hold the SeedQR in front of SeedSigner's camera and your seed loads in seconds. Treat a SeedQR exactly like a written seed backup — it grants full access to your funds.

### Can I use seeds created on other devices?

Yes. Any valid BIP-39 seed phrase works with SeedSigner. You can enter it manually or create a SeedQR from it.

---

## Multi-signature

### Do I need multiple SeedSigners for multi-sig?

No. One SeedSigner can sign with multiple different seeds. Load one seed, sign, discard it, load the next seed, sign again. This is one of SeedSigner's key advantages — you do not need to buy a separate hardware wallet for each cosigner.

### What is a wallet descriptor and why do I need to back it up?

A wallet descriptor defines how your multi-sig wallet is constructed: which public keys, in what order, with what rules. If you lose one seed AND the wallet descriptor, your funds are permanently lost. Always keep a backup of the descriptor. See [Wallet Descriptor](/security/wallet-descriptor.md).

---

## Compatibility

### Which coordinator wallets work with SeedSigner?

Sparrow Wallet, Specter Desktop, BlueWallet, Nunchuk, Keeper, and any wallet that supports PSBT exchange via QR codes. See [Compatible Wallets](/appendices/compatible-wallets.md).

### Does SeedSigner support testnet?

Yes. Change the network in Settings → Advanced → Bitcoin Network → Testnet. Pair it with Sparrow running in testnet mode for practice. See [Using Testnet](/development/testnet.md).

---

## Troubleshooting

### My camera image is upside down

Go to Settings → Advanced → Camera Rotation and try 180° or 0°.

### Sparrow's webcam can't read SeedSigner's QR codes

Try lowering QR Density in SeedSigner's settings (Settings → Advanced → QR Density → Low). Also adjust ambient lighting to reduce screen glare, and press the joystick up/down on SeedSigner to change QR brightness.

### I see "Unknown QR Type" when scanning

The QR code format is not recognized. Make sure you are scanning the correct type (PSBT, SeedQR, or wallet descriptor) and that the QR is clearly visible and well-lit. See [Error Messages](/troubleshooting/error-messages.md).

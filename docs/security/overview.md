# Security model overview

> The core security principles behind SeedSigner and where your responsibilities begin.

SeedSigner is designed around a small number of core security principles. Understanding them helps you make informed decisions about how to use the device.

## Air gap

SeedSigner communicates exclusively through QR codes. The recommended hardware — a Raspberry Pi Zero v1.3 — has **no Wi-Fi, no Bluetooth, and no networking hardware of any kind**. There is no wireless radio to exploit, misconfigure, or compromise.

Every piece of data that enters or leaves the device passes through the camera or the screen, in the form of a QR code. Nothing is transmitted invisibly.

## Statelessness

SeedSigner does not store your keys. When you load a seed phrase, it exists in RAM only. The moment you power off the device, everything is gone.

There is no internal storage to extract, no encrypted vault to crack, and no "forgotten" data lingering on disk. Each session starts completely clean.

## QR communication is auditable

Unlike USB or Bluetooth connections, QR code communication has useful properties:

- **Limited scope** — a QR code can carry only a small, well-defined amount of data.
- **Auditable** — the data in a QR code can be decoded and inspected by anyone with the right tools.
- **Visually obvious** — you can see exactly when data is being exchanged. There is no background process silently sending information.

## Open source

SeedSigner's code is fully open source and available for anyone to review. The community actively audits the software, and you can inspect every line yourself if you choose.

You can also build the software from source rather than trusting a pre-built image, giving you full control over what runs on your device.

## Trade-offs

No security model is perfect. SeedSigner makes deliberate trade-offs in favor of accessibility and affordability. These are discussed honestly in the [Known trade-offs](/security/trade-offs.md) page.

## Related guides

- [Physical security](/security/physical.md) — real-world habits for protecting your device and backups
- [Key storage strategies](/security/key-storage.md) — where and how to store seed backups
- [Known trade-offs](/security/trade-offs.md) — honest discussion of SeedSigner's limitations

## Your responsibilities

SeedSigner handles key generation, transaction signing, and air-gapped communication. Everything else is your responsibility:

- **Seed backup security** — store your seed phrases and wallet descriptors in secure physical locations.
- **Physical environment** — use the device in private, away from cameras and onlookers.
- **Software authenticity** — verify that the software image you flash to the SD card is genuine (check PGP signatures).
- **Transaction verification** — always review transaction details on the SeedSigner screen before approving. Do not rely solely on what your coordinator software displays.

> **Tip:** Security is a practice, not a product. SeedSigner gives you strong tools, but how you use them matters just as much as the tools themselves.

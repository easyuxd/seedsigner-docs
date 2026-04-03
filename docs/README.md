# SeedSigner Documentation

> Open-source, air-gapped Bitcoin signing device built from off-the-shelf hardware.

SeedSigner helps you generate seed phrases, sign Bitcoin transactions, and manage your keys — all without ever connecting to a network. Built on a Raspberry Pi Zero with a camera and LCD display, it communicates exclusively through QR codes.

![SeedSigner in an orange 3D-printed enclosure displaying the home screen, surrounded by a Raspberry Pi Zero, camera module, LCD HAT, SeedQR backup card, seed words notepad, and a gray enclosure](/images/SeedSigner_Device_and_Components.jpg)

## Why SeedSigner?

- **Air-gapped by design** — No Wi-Fi, no Bluetooth, no USB data. The Raspberry Pi Zero v1.3 physically cannot connect to any network.
- **Stateless** — Private keys exist only in RAM while the device is powered on. Pull the plug and they are gone.
- **Affordable** — Total build cost is around $50 with off-the-shelf parts.
- **Open source** — Every line of code and every hardware schematic is publicly auditable.
- **Multi-sig ready** — One device can sign for multiple keys, making multi-signature wallets practical and affordable.

## Get started

| Goal | Go to |
|------|-------|
| Build a SeedSigner from parts | [Hardware Build Guide](/hardware-build/components.md) |
| Install the software on an SD card | [Software Setup](/software-setup/download-and-verify.md) |
| Power on and create your first seed | [Quick-start Checklist](/getting-started/checklist.md) |
| Set up a multi-signature wallet | [Multi-sig Custody Guide](/security/why-multisig.md) |
| Look up a setting | [Configuration Reference](/configuration/basic.md) |

## How it works

```
┌───────────────┐    QR codes    ┌───────────────┐
│   Sparrow /   │  ◄──────────►  │  SeedSigner   │
│  Coordinator  │                │   (signer)    │
│  (networked)  │                │  (air-gapped) │
└───────────────┘                └───────────────┘
        │                              │
        ▼                              ▼
  Bitcoin network              Private keys in RAM
                               (never stored on disk)
```

1. Your wallet coordinator (such as Sparrow) builds an unsigned transaction.
2. It displays the transaction as an animated QR code.
3. SeedSigner scans the QR, shows you the details, and signs it.
4. SeedSigner displays a new QR containing the signature.
5. Your coordinator scans that QR and broadcasts the transaction.

No cables. No wireless. Just light.

## Important security notice

> **Bitcoin transactions are irreversible.** Always verify recipient addresses and amounts before signing. Practice with testnet before using real funds. See [Security Practices](/security/overview.md) for a full guide.

## Project links

- [SeedSigner on GitHub](https://github.com/SeedSigner/seedsigner)
- [SeedSigner website](https://seedsigner.com)
- [Community Telegram](https://t.me/SeedSigner)
- [Sparrow Wallet](https://sparrowwallet.com) (recommended coordinator)

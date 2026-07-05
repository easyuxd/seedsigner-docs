# Get Started

> Start here based on what you want to do. Each path is a guided journey that walks you through the steps in order and links to the detailed [Reference](/reference/hardware/components.md) pages when you want to go deeper.

New to SeedSigner? These journeys take you from a specific goal to a finished result. Pick the one that matches where you are right now — you don't have to read them in order.

## Set up

| Journey | What you'll do |
|---------|----------------|
| **[Build your device](/get-started/build-device.md)** | From loose parts to a working device confirmed at first boot. |
| **[Create your first wallet](/get-started/first-wallet.md)** | Generate a seed, back it up, connect a coordinator, and verify a receive address. *Already have a seed phrase? This covers loading it, too.* |

## Everyday use

| Journey | What you'll do |
|---------|----------------|
| **[Receive bitcoin](/get-started/receive.md)** | Generate a receive address and verify it on the device before sharing it. |
| **[Send bitcoin](/get-started/send.md)** | Build a transaction, review and sign it on SeedSigner, then broadcast. |

## Going further

| Journey | What you'll do |
|---------|----------------|
| **[Recover from backup](/get-started/recover.md)** | Restore access from a paper or SeedQR backup and prove it controls your funds. |
| **[Set up multisig](/get-started/multisig.md)** | Create a multi-key wallet (e.g. 2-of-3) for higher security. |
| **[Use a mobile coordinator](/get-started/bluewallet.md)** | Run your watch-only wallet on your phone with BlueWallet instead of a desktop. |

---

> **Something not working?** Head to [Help & Resources → Troubleshooting](/help/common-issues.md) to diagnose the problem by symptom.

> **Want to look something up directly?** The [Reference](/reference/hardware/components.md) section documents every screen and setting — handy once you know the workflow and just need the details.

## New to Bitcoin self-custody? Read this first

SeedSigner never "connects" to your wallet software the way a USB hardware wallet does. It is **air-gapped**: it shares data only by showing and scanning QR codes. Your phone or computer runs a **coordinator** (such as Sparrow) that builds transactions and talks to the Bitcoin network; SeedSigner only ever holds your keys briefly and signs. This split is what keeps your keys off any networked device — and it's why every journey below moves data back and forth as QR codes rather than over a cable.

> **Practice with testnet first.** Every journey works identically on testnet with free coins and zero risk. See [Using testnet](/contribute/testnet.md), then repeat on mainnet when you're confident.

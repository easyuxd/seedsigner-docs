# Compatible wallets

> Coordinator wallet software tested and supported with SeedSigner.

SeedSigner works with any Bitcoin wallet software that supports PSBT exchange via QR codes.

## Recommended coordinators

| Wallet | Platform | Single-sig | Multi-sig | Testnet | Notes |
|--------|----------|:----------:|:---------:|:-------:|-------|
| [Sparrow Wallet](https://sparrowwallet.com) | Windows, macOS, Linux | Yes | Yes | Yes | Full-featured desktop wallet. Recommended for this guide. |
| [Specter Desktop](https://specter.solutions) | Windows, macOS, Linux | Yes | Yes | Yes | Privacy-focused. Generally requires a full Bitcoin node. |
| [BlueWallet](https://bluewallet.io) | iOS, Android, macOS | Yes | Yes | No | Popular mobile wallet. Does not support testnet. |
| [Nunchuk](https://nunchuk.io) | iOS, Android, Windows, macOS, Linux | Yes | Yes | Yes | Collaborative custody features. |
| [Keeper](https://bitcoinkeeper.app) | iOS, Android | Yes | Yes | Yes | Inheritance planning features. |

## Which should I choose?

Match the coordinator to how you'll actually use the wallet:

| If you… | Choose | Why |
|---------|--------|-----|
| Are new and want the best-documented path | **Sparrow** | Every journey on this site is written against it; full testnet support for risk-free practice |
| Want to manage funds from your phone | **BlueWallet** | Simple mobile watch-only + QR signing — see the [mobile coordinator journey](/get-started/bluewallet.md) |
| Want mobile *and* practice on testnet first | **Nunchuk** | Mobile + desktop apps with testnet support |
| Are setting up collaborative or inheritance custody | **Nunchuk** or **Keeper** | Purpose-built multi-party features |
| Run your own Bitcoin Core node and want it front-and-center | **Specter Desktop** | Designed to pair directly with a local node |

For most users following this documentation, **Sparrow Wallet** is the recommended choice because it:

- Runs on all major desktop platforms.
- Supports both single-sig and multi-sig wallets.
- Has full testnet support for practice.
- Does not require a full Bitcoin node (though it works with one).
- Has excellent QR code scanning support.

You are not locked in. Coordinators only ever hold **public** data — your keys stay on SeedSigner and your backup. You can import the same xpub into several coordinators, or switch later, without touching your seed.

## Coordinator setting in SeedSigner

You can enable or disable specific coordinators in SeedSigner to customize QR code formats:

**Settings → Coordinator Software**

Enable only the coordinators you use. This ensures SeedSigner generates QR codes in the format your wallet expects.

## Using your own node

When your coordinator connects to a public server, you trust that server to provide honest information about the Bitcoin network. Running your own full node (such as Bitcoin Core) eliminates that trust and improves your privacy. This is optional but recommended for advanced users.

Sparrow can connect to:
- Public Electrum servers (default, easiest)
- Your own Electrum server (e.g., Electrs, Fulcrum)
- Your own Bitcoin Core node directly

Specter Desktop is designed to pair with a local Bitcoin Core node.

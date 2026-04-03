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

## Choosing a coordinator

For most users following this documentation, **Sparrow Wallet** is the recommended choice because it:

- Runs on all major desktop platforms.
- Supports both single-sig and multi-sig wallets.
- Has full testnet support for practice.
- Does not require a full Bitcoin node (though it works with one).
- Has excellent QR code scanning support.

If you prefer a mobile-first experience, **Nunchuk** or **Keeper** are strong choices with SeedSigner compatibility.

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

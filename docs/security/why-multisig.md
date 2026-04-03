# Why multi-signature?

> Understand why multi-sig eliminates single points of failure and how SeedSigner makes it affordable.

## The corporate board analogy

Think of a multi-signature wallet like a corporate treasury controlled by a board of directors. The funds are the treasury, and each cosigner holds a key — like a board member holding a vote. Before any funds can move, a majority of the board must approve.

A **2-of-3 multi-sig wallet** means you create 3 total keys, and any 2 of them can authorize a transaction. No single key can move funds on its own.

## What makes multi-sig powerful

Multi-sig gives you **fault tolerance**. There is no single point of failure. If one key is lost, stolen, or destroyed, your funds remain safe and accessible with the other two.

This opens up practical options that single-sig cannot offer:

- **Geographic distribution** — store keys in different physical locations so no single disaster (fire, flood, theft) can take out your wallet.
- **Different hardware profiles** — use different devices or backup formats for each key to avoid a shared vulnerability.
- **Tolerance for mistakes** — you can lose one key OR have one key exposed, and your funds are still protected. In single-sig, either scenario is catastrophic.

## The single-sig dilemma

With a single-signature wallet, you have one private key. To protect against losing it, the natural instinct is to make a second copy. But that second copy doubles your disclosure risk — now there are two places an attacker could find your key.

You are stuck choosing between loss risk and disclosure risk. Multi-sig solves this tension entirely. Each individual key can be stored in exactly one secure location, and you still have redundancy built into the system.

## The honest downsides

Multi-sig is not without trade-offs:

- **More complexity** — you are managing multiple keys, multiple backups, and a wallet descriptor file.
- **More information to track** — losing track of your setup details can be just as dangerous as losing a key.
- **Multiple mistakes can still cause loss** — if you lose 2 of your 3 keys, or lose 1 key AND your wallet descriptor, your funds may be gone forever.

> **Tip:** The wallet descriptor is a critical piece of your backup. Make sure you read the [wallet descriptor backup guide](/security/wallet-descriptor.md) before depositing any funds.

## Multi-sig is not just for experts

If multi-sig feels intimidating, that is the fault of the tools — not you. The concept itself is straightforward, and modern software like Sparrow Wallet has made the process dramatically more accessible.

If you can follow a step-by-step guide, you can set up a multi-sig wallet.

## Why SeedSigner is ideal for multi-sig

Most hardware wallets cost $100 or more. To set up a 2-of-3 multi-sig with traditional hardware wallets, you would need to buy three separate devices — easily $300+.

With SeedSigner, a single device costing around $50 can generate and sign for all three keys. You create each key separately, use it when needed, and discard it from memory when you are done. There is no need to buy three hardware wallets.

This makes multi-sig custody accessible to anyone, not just those willing to spend hundreds of dollars on hardware.

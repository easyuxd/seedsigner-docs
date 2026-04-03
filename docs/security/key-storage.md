# Key storage strategies

> Practical strategies for storing seed backups — media, locations, copies, and tamper evidence.

How and where you store your seed backups is one of the most important decisions in your custody setup.

## Storage media

### Paper

- **Pros:** Free, simple, no special tools needed.
- **Cons:** Vulnerable to fire, water, and ink degradation over time.
- **Best practices:** Use archival-quality pen and paper. Store in a waterproof, fireproof container. Consider lamination.

### Metal

- **Pros:** Resistant to fire, water, and physical degradation. Long-term durability.
- **Cons:** Requires a metal backup kit (steel washers, plates, or stamps). Takes more time to create.
- **Recommendation:** Strongly recommended for any seed protecting significant value. Options include stamped steel washers, engraved plates, and commercial seed storage products.

### SeedQR

- **Pros:** Fast loading into SeedSigner (seconds vs. minutes for manual entry). Compact.
- **Cons:** Must be transcribed carefully. Can be printed or hand-drawn. Same fire/water vulnerability as paper unless stamped onto metal.
- **Best practices:** Always verify your SeedQR using SeedSigner's "Confirm SeedQR" feature. Never scan a SeedQR with any internet-connected device.

---

## How many copies?

This is a personal decision with trade-offs:

- **One copy per key** (recommended for multi-sig) — If you use a multi-signature wallet, you can tolerate the loss of one key. Having only one copy of each key minimizes disclosure risk. If one copy is lost, your funds are still accessible with the remaining cosigners.

- **Two copies per key** — Halves the risk of loss but doubles the risk of disclosure. You must now secure two locations per key. More appropriate for single-signature setups where losing the one key means losing everything.

> **Tip:** In a multi-sig wallet, the fault tolerance is built into the quorum structure. You do not need redundant copies of each key — that is what multi-sig is for.

---

## Where to store keys

Distribute your key backups across geographically separate, physically secure locations:

| Location type | Pros | Cons |
|--------------|------|------|
| **Home safe** | Convenient access | Vulnerable to home intrusion, fire |
| **Bank safe deposit box** | High physical security | Rogue employees, bank access hours, not fully private |
| **Trusted person's safe** | Geographic distribution | Requires trust, availability |
| **Off-site secure storage** | Geographic redundancy | Access logistics |

### Geographic distribution

Consider how far apart your key storage locations should be, based on how often you expect to access funds:

- **Same city** — convenient but vulnerable to regional disasters.
- **Different cities** — good balance of security and accessibility for cold storage.
- **Different countries** — maximum redundancy but significant access overhead.

For most cold-storage users making 1--2 transactions per year, different cities within the same country is a practical default.

---

## Tamper evidence

You cannot always be certain that no one has accessed your stored seeds while you are away. Tamper-evident measures help you detect unauthorized access:

- **Tamper-evident bags** — use the same sealable evidence bags that law enforcement uses. Sign or initial the seal with a unique marking.
- **Security tape** — apply over the opening of a container. Any attempt to peel it leaves a visible "VOID" pattern.
- **Sealed containers** — a small lockbox adds a physical barrier, though it signals that something valuable is inside.

Make it a habit to do periodic **key checks** — visit your storage locations and verify that seals are intact, backups are legible, and nothing has been disturbed.

---

## Passphrase as an additional layer

A BIP-39 passphrase adds protection against seed disclosure. Even if someone finds and copies your seed words, they cannot access your funds without also knowing the passphrase.

Store the passphrase **separately** from the seed words. If they are stored together, the passphrase provides no additional security.

> **Warning:** If you use a passphrase and forget it, or lose the only copy, the funds protected by that passphrase are permanently inaccessible. Treat passphrase backup with the same care as seed backup.

---

## Decoy funds (optional)

Some users deposit a small amount of Bitcoin into a single-signature wallet derived from one of their seeds (without the passphrase). If coerced to hand over funds, this "decoy wallet" can be presented as the full extent of your holdings.

This is a well-known technique, so its effectiveness depends on the threat model. The amount should be large enough to seem plausible.

---

## Summary for a 2-of-3 multi-sig setup

| Item | Copies | Storage |
|------|--------|---------|
| Seed 1 | 1 (on metal) | Home safe |
| Seed 2 | 1 (on metal) | Bank safe deposit box |
| Seed 3 | 1 (on metal) | Trusted person's safe (different city) |
| Wallet descriptor | 2--3 copies (printed + digital) | With each seed, and optionally on a computer |

This distribution ensures that:
- Losing any single location does not lock you out.
- Compromising any single location does not give an attacker access (they need 2 of 3 seeds).
- The wallet descriptor is available wherever you might need it for recovery.

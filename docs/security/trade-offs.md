# Known trade-offs

> Honest discussion of SeedSigner's security limitations and how to manage them.

Every security tool makes trade-offs. SeedSigner is no exception. This page addresses the most common criticisms so you can make informed decisions.

## 1. Direct access to seed phrases increases disclosure risk

**The concern:** Unlike hardware wallets that store keys internally, SeedSigner requires you to enter your seed words each time you sign. This means your seed is exposed during use.

**The response:** SeedSigner is designed for cold storage. You should be accessing your keys only a few times per year — not daily. The exposure window is brief and infrequent.

You can further reduce risk by:

- Adding a **passphrase** to your seed, so the seed words alone are not sufficient to access funds.
- Being deliberate about your **physical environment** — work in private, shield the screen, and discard the seed from memory as soon as you finish.

## 2. One device signs for multiple keys

**The concern:** In a multi-sig setup, using the same SeedSigner for all three keys means a single compromised device could theoretically sign with multiple keys.

**The response:** This is a deliberate trade-off favoring cost savings and simplicity. A single $50 device makes multi-sig accessible to everyone, rather than requiring $300+ in hardware wallets.

If this concerns you, mix in hardware from different manufacturers for one or more of your cosigner keys. SeedSigner works alongside other signing devices in a multi-sig setup without any issues.

## 3. Large Linux attack surface

**The concern:** SeedSigner runs on Linux, which is a large and complex operating system with a broad attack surface.

**The response:** SeedSigner operates in complete isolation. There is no network connection, no USB data exchange, and no Bluetooth. A vulnerability in the Linux kernel would need a delivery mechanism, and the air gap eliminates remote delivery entirely.

The SD card image is the trust boundary. If you verify the image before flashing it, the attack surface is contained to what is on that card.

## 4. The air gap is security theatre

**The concern:** Some argue that an air gap provides only an illusion of security and does not meaningfully protect against sophisticated attacks.

**The response:** The air gap is not a silver bullet, but it is far from theatre. QR code communication is:

- **Limited in scope** — only small, well-defined data payloads can pass through.
- **Auditable** — QR contents can be decoded and inspected.
- **Visually obvious** — you can see exactly when data is being transferred.

For an air-gap attack to succeed, **both** SeedSigner and your coordinator software (such as Sparrow) would need to be independently compromised and coordinating with each other through QR codes. This is an extraordinarily difficult attack to execute.

## 5. No secure boot — how do you know the software is genuine?

**The concern:** The Raspberry Pi does not support secure boot, so there is no hardware-level guarantee that the software has not been tampered with.

**The response:** You are the validation mechanism. Before flashing the SD card:

- Download the official release from the SeedSigner GitHub repository.
- **Verify the PGP signature** on the release to confirm it was signed by the project maintainers.
- If you want the highest assurance, **build the software from source** yourself and compare the result.

This requires effort, but it puts verification entirely in your hands rather than trusting a hardware mechanism you cannot inspect.

## 6. Evil maid attack

**The concern:** Someone with physical access to your SeedSigner could replace the SD card with a malicious version that leaks your seed words through crafted QR codes.

**The response:** Mitigations include:

- Store your SeedSigner in a secure location when not in use.
- Use **tamper-evident packaging** (sealed bags with your initials) so you can detect if someone has accessed the device.
- If you have any doubt about the device's integrity, **re-flash the SD card** from a verified image before use.

Since SeedSigner is stateless, re-flashing the SD card returns the device to a known-good state with zero data loss.

## 7. The Broadcom chip is closed source

**The concern:** The Broadcom system-on-chip (SoC) at the heart of the Raspberry Pi contains proprietary code that cannot be audited.

**The response:** There is no known vulnerability in the Broadcom SoC that would affect signing operations. More importantly, the supply chain argument makes targeted exploitation impractical: tens of millions of Raspberry Pi boards are manufactured and sold for countless purposes. Only a minuscule fraction ever become Bitcoin signing devices. Compromising the chip at the manufacturing level to target Bitcoin users would be extraordinarily wasteful and easy to detect.

## 8. Pi firmware is partially closed source

**The concern:** The Raspberry Pi's boot firmware includes closed-source binary blobs that cannot be fully audited.

**The response:** The same supply chain reasoning applies. Any exploit embedded in the Pi firmware would need to affect the entire global supply of Raspberry Pi boards — not just the handful used for Bitcoin signing. The firmware is shared across millions of devices used for education, industrial automation, media centers, and countless other applications. A targeted attack through this vector is impractical at scale.

---

These trade-offs are real, and you should weigh them against your own threat model. For most users practicing standard cold storage with reasonable physical security, SeedSigner provides a strong and cost-effective security profile.

> **Tip:** Security is about managing risk, not eliminating it. Understanding these trade-offs puts you in a better position than ignoring them.

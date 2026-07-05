# Image download & verification

> Download the SeedSigner software image and verify its authenticity before flashing.

Before you power on your SeedSigner device, you need to download the software image and verify that it has not been tampered with. This step is essential — take it seriously.

## Why verification matters

With Bitcoin self-custody, **you are your own security team**. There is no company or help desk standing between you and your funds. A compromised software image could silently steal your private keys the moment you load a seed.

By verifying the software yourself, you confirm that the image you downloaded is the exact file the SeedSigner maintainer published. No modifications, no surprises.

> **Tip:** If you're new to PGP verification, take the time to learn — it's an important skill for Bitcoin self-custody. The few minutes you invest now will serve you well for years.

## Download the release image

1. Go to the official SeedSigner GitHub releases page:  
   [https://github.com/SeedSigner/seedsigner/releases](https://github.com/SeedSigner/seedsigner/releases)
2. Download the latest `.img` file that matches your hardware (Raspberry Pi Zero).
3. Download the corresponding **signature/hash file** published alongside the image.

Do not download SeedSigner images from any other source. Always use the official GitHub repository.

## Verify the download

The SeedSigner maintainer publishes a PGP-signed message containing the SHA256 hashes for each release. Verification answers two separate questions, and you need both:

1. **Is the signed hash list authentic?** (Was it really published by the maintainer?) → the *signature* check.
2. **Is my file the one that was signed?** (Not corrupted or swapped?) → the *hash* comparison.

You'll need GPG installed: it ships with most Linux distros, comes with [GPG Suite](https://gpgtools.org) on macOS, and with [Gpg4win](https://gpg4win.org) on Windows.

### Step 1: Import the maintainer's public PGP key

Download the maintainer's public key (published in the SeedSigner GitHub repository) and import it into your local keyring:

```bash
gpg --import seedsigner_pubkey.asc
```

GPG confirms with a line like `key <KEY-ID>: public key "SeedSigner <email>" imported`.

### Step 2: Check the key's fingerprint against independent sources

Importing a key proves nothing by itself — an attacker who could tamper with your download could also serve you a fake key. What ties the key to the real maintainer is its **fingerprint** (a 40-character hex string). Display it:

```bash
gpg --fingerprint
```

Now compare that fingerprint against **at least two independent places** where the maintainer has published it — for example the SeedSigner GitHub repository *and* the project's posts or profiles on other platforms. The more independent channels agree, the harder the fingerprint is to fake. If the fingerprints differ *anywhere*, stop and ask in the community channels before proceeding.

> **Tip:** This step is the heart of the whole procedure. Signature math is automatic; deciding to trust the key is the human part. Do it once, carefully, and future releases verify against the same key.

### Step 3: Verify the PGP signature on the hash file

With the key imported and fingerprint-checked, verify that the signed hash list really was signed by it:

```bash
gpg --verify <signature-file>
```

A successful check looks like:

```
gpg: Good signature from "SeedSigner <email>"
```

Two common messages and what they mean:

- `WARNING: This key is not certified with a trusted signature!` — **this is normal and OK.** GPG is telling you that *you* haven't formally marked the key as trusted in your keyring. Your trust comes from the fingerprint check in Step 2, so you can proceed.
- `BAD signature` — **stop immediately.** The file was altered after signing, or was signed by something else. Do not use the image; re-download and re-verify, and report it if the failure repeats.

### Step 4: Compare the SHA256 hash

Finally, confirm your `.img` file matches the hash inside the signed file. Generate your file's hash:

**Linux / macOS:**
```bash
sha256sum seedsigner_<version>.img
```

**Windows (PowerShell):**
```powershell
Get-FileHash seedsigner_<version>.img -Algorithm SHA256
```

Compare the output to the hash listed for your file in the signed message — it must match **exactly, every character**. On Linux/macOS you can automate the comparison by running `sha256sum -c` against the hash file, which prints `OK` per file.

If the hashes don't match, your download is corrupted or tampered with. Delete it, download again, and repeat. 

> **Warning:** If the hash does not match after a second download, do not use the image. Report the issue on the SeedSigner GitHub repository.

## If verification fails: quick reference

| What you see | What it means | What to do |
|--------------|---------------|------------|
| `Good signature` + "not certified" warning | Success — the warning is expected (see Step 3) | Proceed |
| `BAD signature` | The signed file was modified | **Stop.** Re-download; report if it repeats |
| `Can't check signature: No public key` | The maintainer's key isn't in your keyring | Do Steps 1–2, then re-verify |
| Fingerprint doesn't match a published source | Possible fake key | **Stop.** Ask in community channels |
| SHA256 mismatch | Corrupted or tampered image file | Re-download; **stop** if it repeats |

## Build from source

If you want maximum assurance that the software is exactly what the source code says it is, you can build the image yourself from source. This eliminates any trust in the pre-built release file — you verify the *code* instead of the *binary*.

See the build instructions in the [SeedSigner GitHub repository](https://github.com/SeedSigner/seedsigner).

## Next step

Once you have a verified image file, you're ready to [write the SD card](/reference/software/flash-sd-card.md).

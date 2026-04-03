# Download and verify

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

The SeedSigner maintainer publishes a PGP-signed message containing a SHA256 hash for each release file. Verification has two parts: confirming the signature is authentic, and confirming your file matches the signed hash.

### Step 1 — Import the maintainer's public PGP key

If you haven't already, import the maintainer's public key into your keyring. The key is available on the SeedSigner GitHub repository.

```bash
gpg --import seedsigner_pubkey.asc
```

### Step 2 — Verify the PGP signature

Use GPG to verify that the signature file was actually signed by the maintainer's key:

```bash
gpg --verify <signature-file>
```

You should see a message confirming a **Good signature**. If GPG reports a bad signature or an unknown key, stop — do not use the image.

### Step 3 — Compare the SHA256 hash

Generate the SHA256 hash of your downloaded `.img` file and compare it to the hash in the signed message:

**Linux / macOS:**
```bash
sha256sum seedsigner_<version>.img
```

**Windows (PowerShell):**
```powershell
Get-FileHash seedsigner_<version>.img -Algorithm SHA256
```

The output must match the hash in the signed file exactly. If it doesn't, your download may be corrupted or tampered with — download the file again and repeat the process.

> **Warning:** If the hash does not match after a second download, do not use the image. Report the issue on the SeedSigner GitHub repository.

## Build from source

If you want maximum assurance that the software is exactly what the source code says it is, you can build the image yourself from source. This eliminates any trust in the pre-built release file.

See the build instructions in the [SeedSigner GitHub repository](https://github.com/SeedSigner/seedsigner).

## Next step

Once you have a verified image file, you're ready to [write the SD card](/software-setup/write-sd-card.md).

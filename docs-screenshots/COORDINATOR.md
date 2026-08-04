# Coordinator screenshots

The `Sparrow_*.png` files in `docs/images/`. They close audit findings **A6, A9,
B10 and X-1** — the coordinator half of every journey, which had zero screenshots
before.

Nothing in the emulator can produce these: they are a desktop GUI, not a 240×240
device framebuffer. So unlike everything else in this directory, they are
captured by hand rather than rendered. This file is the procedure, so the set can
be rebuilt or extended without re-deriving it.

## What was captured

Sparrow Wallet **2.5.3**, Windows, light theme, **Testnet3**, window sized
1200×800 on a 2560×1440 display at 100% scaling. Captures are 1:1 pixels, cropped
to the region the surrounding step is about — no downscaling.

| File | Page | Shows |
|---|---|---|
| `Sparrow_FileNewWallet.png` | first-wallet 4.1, multisig 2.2 | File menu, New Wallet |
| `Sparrow_WalletName.png` | first-wallet 4.2 | name dialog, "My Single-Sig" |
| `Sparrow_WalletSettings.png` | first-wallet 4.3-4, recover 3.2 | Single Signature + Native Segwit (P2WPKH), four keystore buttons |
| `Sparrow_AirgappedHardwareWallet.png` | first-wallet 4.6, multisig 3.3 | airgapped device list, SeedSigner + **Scan…** |
| `Sparrow_ScanKeystoreQR.png` | first-wallet 4.7, multisig 3.4 | the webcam view reading the device's xpub QR |
| `Sparrow_KeystoreImported.png` | first-wallet 4.8, recover 3.2 | fingerprint `b5aa2761`, derivation `m/84'/1'/0'`, the account tpub |
| `Sparrow_WalletPassword.png` | first-wallet 4.9, multisig 4.2 | **No Password** |
| `Sparrow_ReceiveAddress.png` | first-wallet 4, receive 1 | `tb1qwp75hxq…` at `m/84'/1'/0'/0/5` + QR |
| `Sparrow_MultisigPolicy.png` | multisig 2.4-5 | Multi Signature HD, Native Segwit (P2WSH), **M of N 2 / 3** |
| `Sparrow_MultisigKeystores.png` | multisig 4 | `wsh(sortedmulti(2,…))` and the three cosigner tabs |
| `Sparrow_BackupDescriptorPrompt.png` | multisig 5, descriptor.md | Sparrow's own "back this up" prompt with the full descriptor |
| `Sparrow_ExportWalletSpecter.png` | multisig 5, descriptor.md | Export Wallet, Specter Desktop row |
| `Sparrow_DescriptorQR.png` | multisig 5, descriptor.md | the descriptor as a QR |
| `Sparrow_TransactionReview.png` | send 1, multisig/spending 1 | the journey PSBT, signing wallet **My Single-Sig** |
| `Sparrow_TransactionSigning.png` | first-wallet 7.1, send 1, psbt-signing 1 | Show QR / Scan QR / Sign |
| `Sparrow_ScanSignedPSBT.png` | first-wallet 7.5, send 3, psbt-signing 7, spending 2 | the webcam view reading the signed PSBT back |
| `Sparrow_PSBTQR.png` | send 1, psbt-signing 1 | the unsigned PSBT as a QR |
| `Sparrow_BroadcastTransaction.png` | first-wallet 7.5, send 4, psbt-signing 9, spending 4 | signature complete, **Broadcast Transaction** |

Every value on screen comes from `fixture.py`, so the coordinator screenshots and
the device screenshots describe the same wallet and the same transaction. In
particular the Receive tab was advanced to **index 5** so it shows the exact
address `SeedAddressVerificationSuccessView.png` reports as verified.

## How to rebuild the two wallets

Both were created by pasting an **output descriptor** into
*Settings → Script Policy → Descriptor → Edit…*, which is the only way to load
exact keys without a webcam. Sparrow then derives the fingerprints and derivation
paths itself, so nothing on screen is typed in by hand.

```bash
python -c "import sys; sys.path.insert(0,'docs-screenshots'); import fixture; \
  print(f'wpkh([{fixture.FINGERPRINT}/84h/1h/0h]{fixture.XPUB}/<0;1>/*)')"
python -c "import sys; sys.path.insert(0,'docs-screenshots'); import fixture; \
  print(fixture.MULTISIG_DESCRIPTOR)"
```

1. `Tools → Restart In → Testnet3`, then connect to a public server.
2. `File → New Wallet` → "My Single-Sig" → paste the `wpkh(...)` descriptor →
   label the keystore `SeedSigner` → **Apply** → **No Password**.
3. `File → New Wallet` → "My Multisig" → **Multi Signature HD** → paste the
   `wsh(sortedmulti(2,...))` descriptor → label the keystores `SeedSigner 1/2/3`
   → **Apply** → **No Password**.
4. Receive tab → **Get Next Address** ×5 to reach index 5.
5. For the send screens, `File → Open Transaction → From Text…` and paste
   `fixture.PSBT_BASE64`. Sparrow recognises it as belonging to My Single-Sig.
   For the broadcast screen, sign it first with the fixture seed and load the
   result via **Load Transaction**:

```python
from embit.psbt import PSBT
from embit.bip32 import HDKey
from embit import bip39
psbt = PSBT.from_string(fixture.PSBT_BASE64)
psbt.sign_with(HDKey.from_seed(bip39.mnemonic_to_seed(" ".join(fixture.MNEMONIC)),
                               version=fixture.EMBIT_NETWORK["xprv"]))
print(psbt.to_string())
```

**The PSBT's inputs are synthetic**, so the transaction is unbroadcastable by
construction. That is deliberate: the screen can be captured with the Broadcast
button live, and pressing it can never spend anything.

## Verifying a capture

The same rule as the device set: automated checks confirm a file exists and is
referenced, not that it shows the right thing. Read the values.

`Sparrow_DescriptorQR.png` is machine-checkable, and was checked — it decodes to
the Specter-format descriptor carrying all three fixture fingerprints:

```bash
python -c "from pyzbar import pyzbar; from PIL import Image; \
  print(pyzbar.decode(Image.open('docs/images/Sparrow_DescriptorQR.png'))[0].data.decode())"
```

## Re-shot from a real scan

The original set was captured on a machine with no camera, so the keys were
loaded by pasting a descriptor and the keystore's `Type:` row read
"Watch Only Wallet". Both keystore captures have since been **re-shot from an
actual QR scan** off the emulator running [live_emulator.py](live_emulator.py),
so `Type:` now reads **Airgapped Wallet (Seedsigner)** and the crops start above
that row rather than below it:

| File | Shows |
|---|---|
| `Sparrow_KeystoreImported.png` | Type / Label / `b5aa2761` / `m/84'/1'/0'` / account tpub |
| `Sparrow_MultisigKeystores.png` | `wsh(sortedmulti(2,…))`, the three cosigner tabs, and cosigner 1's Type row |

The scanned tpub is byte-identical to the descriptor-loaded one, so nothing else
in the set had to move.

## The scan dialog

Sparrow reaches its webcam view from two places — *Airgapped Hardware Wallet →
SeedSigner → Scan…* and *Signatures → Scan QR* on an open transaction. Both
render the same 662×529 dialog; captured empty, a pixel diff outside the video
area is 901 px, all of it the progress bar caught at a different phase of its
animation. **What distinguishes the two files is the QR in the viewport**, so
each is wired to its own step:

| File | Page | Viewport decodes to |
|---|---|---|
| `Sparrow_ScanKeystoreQR.png` | first-wallet 4.7, multisig 3.4 | `UR:CRYPTO-ACCOUNT/1-5/…` — the fixture xpub |
| `Sparrow_ScanSignedPSBT.png` | first-wallet 7.5, send 3, psbt-signing 7, spending 2 | `UR:CRYPTO-PSBT/1-22/…` — the signed journey PSBT |

The viewport is composited by hand — the coordinator-side half of audit **X-2**.
[camera_qrs.py](camera_qrs.py) renders the QR that belongs in each frame, built
from `fixture.py` and encoded by SeedSigner's own `UrXpubQrEncoder` /
`UrPsbtQrEncoder`, so the format is what the device really emits and the payload
is the real fixture value. Every composited frame in the library decodes:

```bash
python -c "from pyzbar import pyzbar; from PIL import Image; \
  print(pyzbar.decode(Image.open('docs/images/Sparrow_ScanKeystoreQR.png'))[0].data.decode())"
```

## Prose corrected against the real UI

Reading the actual screens turned up four claims that were wrong:

| Was | Is |
|---|---|
| "Find SeedSigner and click **Import / Scan**" | SeedSigner offers **Scan…** only — no file import |
| "Under Policy Type, select **Multi Signature**" | the option reads **Multi Signature HD** |
| "**Tools → Restart in Testnet**" | **Tools → Restart In → Testnet3** |
| "the **Keystore** panel… **Xpub / Watch Only Wallet**" | the button reads **Watch Only Wallet** |

## Not covered: BlueWallet

`get-started/bluewallet.md` steps 2, 4 and 5 are still text-only. BlueWallet is a
mobile app with no Windows desktop build, so it is a separate capture project on
a phone. Audit A10/A11 (the *device*-side BlueWallet screens) were already closed
in Phase 3 and are unaffected.

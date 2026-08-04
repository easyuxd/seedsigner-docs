# Screenshot regeneration plan

Companion to [screenshot-audit.md](screenshot-audit.md). The audit says *what* is
wrong; this says *how an agent fixes it*.

## Decisions

| Decision | Choice |
|---|---|
| Scope | Full regen of the image library from code |
| Canonical data | New docs-only fixture seed; prose moves to match it |
| Code home | `docs-screenshots/` inside this repo |
| Network | Testnet |
| Prose reconciliation | Everything the audit names |
| Coordinator screenshots | Deferred to Phase 5; Sparrow now done, BlueWallet still open |

---

## Why this is tractable

The emulator's batch generator
(`seedsigner-app/tests/screenshot_generator/generator.py`) is **headless,
deterministic, pure Python**. Every screen is one declarative entry:

```python
ScreenshotConfig(SomeView, dict(seed_num=0), screenshot_name="Foo", run_before=cb)
```

No window opens, no clicking, no timing. Producing a custom screen is a
code-editing task, which is what an agent is good at — as opposed to driving a
GUI, which is what it is bad at.

### Three facts established before planning

**1. The current library has two origins.** 55 of 144 filenames match generator
output exactly. The other 89 are hand-captured live shots — and they are
precisely the odd-sized ones (236–241 px, 290–298 px). Only 59 files are clean
240×240. That is finding X-6, fully explained: it is a provenance split, not a
cropping accident.

**2. Hand-captured states are scriptable after all.** Every View funnels through
one method, `View.run_screen(Screen_cls, **kwargs)` at `views/view.py:107`, and
`ButtonListScreen` carries `selected_button: int = 0`. Monkeypatching
`run_screen` to merge in extra screen kwargs yields any "menu row N highlighted"
screen deterministically. This eliminates the entire hand-capture category,
including SS-1 (Sparrow highlighted) and MS-2 (Multisig highlighted).

**3. Fingerprint `593c4724` is unreproducible.** Computed from the generator's
own fixtures:

| Fixture | Fingerprint | Appears in |
|---|---|---|
| `mnemonic_12` + passphrase | `720d2d65` | `SeedExportXpubDetailsView.png` (SS-4) |
| `mnemonic_24`, no passphrase | `8c65eb9f` | `SeedFinalizeView.png` (SS-2) |
| `mnemonic_12b` (abandon×11) | `73c5da0a` | multisig descriptor, address explorer |
| `593c4724` (prose canon) | — | **matches nothing** |

It came from a hand-capture with a seed no longer on hand. A fingerprint cannot
be ordered — you pick a seed and it falls out — and brute-forcing 4 bytes is
~2³² BIP32 derivations. Hence: the prose moves, not the image.

---

## Canonical fixture

One seed for the entire single-sig journey (`build-device` → `first-wallet` →
`receive` → `send` → `recover`). Derived from fixed entropy so it is rebuildable
from the plan alone:

```python
ent = hashlib.sha256(b"seedsigner-docs canonical fixture v1").digest()
mnemonic = bip39.mnemonic_from_bytes(ent)   # 24 words
```

```
approve hip ball squirrel melt entry bunker thunder mixture soup science depend
piece enrich echo climb assist know alone jaguar obey history unknown aspect
```

| Value | Testnet |
|---|---|
| Master fingerprint | `b5aa2761` |
| Derivation | `m/84'/1'/0'` |
| Account xpub | `tpubDCnUzqwEMfKNuVjU…7qcMA6` |
| Receive `0/5` | `tb1qwp75hxqf7hx5qx2gvvekarhacvf9fx0mw7p4sl` |
| Multisig 2-of-3 | `f79a2f18` / `7b764b64` / `86442e23` |

Index 5 keeps continuity with the existing captures, whose "receive address
index 5" the docs already reference (audit SS-6).

The fingerprint is network-independent, so `b5aa2761` is the single value the
whole docset can quote — mainnet or testnet, journey or reference.

**Multisig (2-of-3)** uses `…fixture v1 msig 1|2|3` as entropy for three sibling
seeds, replacing the upstream 1-of-2 descriptor. Closes MS-3.

Decisions this settles:

- **SS-5** — 24 words, matching `first-wallet.md:73`.
- **SS-6** — the journey address becomes a stated value, not a screenshot-only secret.
- **SS-7 / D9** — testnet renders amounts green (`TESTNET_COLOR = "#00F100"`,
  `gui/components.py:39`) and labels them tBTC/tsats. The "visual indicator"
  `contribute/testnet.md:56` claims is real, and appears on any view showing an
  amount. Screenshot it there.

**Fixture safety:** published, well-known, testnet-only, and never to hold value —
the same posture as the upstream generator's fixtures.

---

## Architecture

```
seedsigner-docs/
└── docs-screenshots/
    ├── README.md          how to run it, how to add a screen
    ├── fixture.py         the canonical seed(s), PSBT, descriptor, address, network
    ├── manifest.py        every screen: View + kwargs + OUTPUT FILENAME
    ├── shim.py            RPi mocks, ScreenshotRenderer wiring, run_screen patch
    └── generate.py        entry point → writes straight into docs/images/
```

Run with the emulator's existing venv; app location via `$env:SEEDSIGNER_APP`:

```bash
python docs-screenshots/generate.py --all
```

Three properties that make this the right shape:

- **Upstream is never edited.** The script `sys.path`-inserts `seedsigner-app/src`
  and imports read-only, reusing the upstream `ScreenshotRenderer` from
  `tests/screenshot_generator/utils.py`. Emulator upgrades cannot clobber it, and
  the RPi-module mocks are replicated in `shim.py` because they must run before
  any SeedSigner import.
- **`manifest.py` is the source of truth for filenames.** `screenshot_name` is
  arbitrary, so the 70 currently-referenced images keep their existing names —
  **zero markdown churn** on already-wired images. Only new captures get new
  names. It also absorbs the upstream renames (`SeedWordsBackupTestView` →
  `SeedBackupTestView.png`) that would otherwise force a rewrite of every ref.
- **No pytest.** Upstream needs it only for locale parametrization. The docs
  script drives the views directly and takes `--locale` as a plain argument.

### The `screen_kwargs` mechanism

`View.run_screen` is patched for the duration of one screenshot, so
`manifest.py` can inject any Screen field — chiefly `selected_button`. This is
the single unlock for all 51 orphaned `*SelectView.png` shots plus SS-1 and MS-2.

Rows are selected **by label, not by index**:

```python
screen_kwargs=highlight("Sparrow")
```

Phase 1 shipped with raw indices first and immediately proved why that is wrong:
`selected_button=1` on the settings menu rendered *Persistent settings*, not
*Coordinator software* — a perfectly plausible screenshot of the wrong row, and
exactly the failure the audit had to catch by eye. `highlight()` resolves the
label against the Screen's own `button_data` and raises on a miss or an
ambiguous match:

```
ValueError: select_label 'Sparow' not found. Rows are:
  ['BlueWallet', 'Nunchuk', 'Sparrow', 'Specter Desktop']
```

With 51 settings screens to wire up in Phase 3, index drift would otherwise be
the most likely source of silently wrong images in the whole effort.

---

## Phases

### Phase 1 — Pipeline ✅ done

`docs-screenshots/` built and proven on an 11-shot subset — see its
[README](docs-screenshots/README.md). Every mechanism the full regen depends on
is demonstrated:

| Mechanism | Proof |
|---|---|
| Fixture flows into rendered screens | `SeedFinalizeView` reads `b5aa2761` (SS-2) |
| Row highlighting | Sparrow highlighted (SS-1), Multisig highlighted (MS-2) |
| Label resolution fails loudly | typo and ambiguous-match both raise |
| Testnet throughout | `tb1qwp7…`, "Single Sig - Native Segwit (Testnet)" |
| Upstream untouched | app imported read-only; renderer loaded by file path |
| Size guarantee | all 11 verified 240×240 |

Output stages to `docs-screenshots/out/` (gitignored); `--out docs/images`
overwrites the live library and is deliberately not the default.

#### The journey PSBT

Built and verified — 17 shots now render. `send.md` carries the audit's
highest-severity gaps (A1–A3, A7: the reader is told to scrutinise a review
screen they have never been shown), and upstream's `BASE64_PSBT_1` could not
fill them because it is signable by `abandon x11`, not by the journey seed.

`fixture.build_psbt()` constructs an unsigned 2-input, 2-output testnet spend
from the fixture wallet: 350,000 in → 200,000 to an external address, 148,500
change, 1,500 fee. Amounts are chosen so `PSBTMathView`'s arithmetic is checkable
by eye.

Three independent confirmations that the PSBT parses as intended, rather than
merely rendering:

- `PSBTChangeDetailsView` shows `b5aa2761: Change #0` and **"Address verified!"** —
  the change output was recognised as ours and its derivation checked.
- `PSBTSelectSeedView` lists `b5aa2761` with **no `(?)`** while all three multisig
  cosigners carry one. `(?)` marks a seed that cannot sign this PSBT, so
  SeedSigner itself confirms the signer.
- `PSBTOverviewView` and `PSBTMathView` render amounts as green **tSats**,
  closing D9/SS-7 on the screens that actually carry an amount.

### Phase 2 — Full regen ✅ done

175 shots, every one at 240×240, from the canonical fixture on testnet. X-6 is
closed by construction. The library went from 144 files (59 clean 240×240) to
185 files, all uniform.

Includes the targeted re-shoots the audit calls for:

| Finding | Fix in manifest |
|---|---|
| SS-1 | `SeedExportXpubCoordinatorView`, `selected_button` → Sparrow |
| SS-2 | `SeedFinalizeView` at `b5aa2761`, new filename for `recover.md` |
| SS-4 | `SeedExportXpubDetailsView` at the journey fingerprint — **but see the correction below** |
| MS-1 | address-verification pair with `sig_type=MULTISIG` |
| MS-2 | `SeedExportXpubSigTypeView`, `selected_button` → Multisig |
| MS-3 | 2-of-3 descriptor from the three msig fixture seeds |
| A12 | `OpeningSplashView` + `MainMenuView_RemoveSDCardToast` — both already exist upstream, never wired in |
| D9 | any amount-bearing view on testnet (green tBTC) |

#### Correction to audit finding SS-4

The audit read the `zpub…` prefix on `SeedExportXpubDetailsView.png` as evidence
that "the whole xpub-export series was captured in a BlueWallet session," and
treated it as corroboration for SS-1.

That inference is wrong. The SLIP-132 version comes from
`Seed.detect_version()` → `bip32.detect_version(derivation_path, network)`
(`models/seed.py:128`, called at `views/seed_views.py:939`) — **derivation path
and network only**. BIP-84 single-sig always serialises as `zpub` on mainnet and
`vpub` on testnet, whichever coordinator is selected. Verified by rendering with
`coordinator="spa"`: still `vpub`.

So there is nothing to fix about the serialisation, and Sparrow reads SLIP-132
fine. SS-4 reduces to the fingerprint alone. **SS-1 is unaffected** — it rests on
the directly visible highlighted row, not on this inference.

Two further mechanisms the manifest needed beyond `screen_kwargs`:

- **`screen_mutate`** — a hook running between Screen construction and display,
  for state that lives on a component rather than a Screen field.
  `PowerIconSelectedScreen` (D6) needs `TopNav.is_selected`, plus clearing the
  tiles so two things aren't highlighted at once.
- **`toast`** — the SD-card notifications (A12) draw over an already-rendered
  screen, so the toast runs after `ScreenshotComplete` and saves again.

#### Still preserved, not generated

10 files. Live camera frames (`AddressVerificationsCameraView`, `SeedPSBTCameraView`,
`SeedCameraEntropyView`, `SeedEntropyPreviewView`, `SeedQRScan`) have no video
source headlessly — upstream carries the same limitation. Animated QR displays
(`SeedExportXpubQRView`, `AddressExplorerQRView`) cycle frames; upstream leaves
them out for the same reason. Three are hardware photos and brand assets.

**X-2 (the blank camera frames)** is closed by hand rather than by the manifest —
see Phase 5. The viewports are composited, so the frames now show what the device
is actually looking at instead of black.

#### A Windows trap worth recording

The two `SelectVIew` → `SelectView` typo fixes differ only by letter case. On a
case-insensitive filesystem those are *the same file*, so the retire step deleted
freshly-rendered content. `retire()` now skips any name that case-insensitively
matches a generated filename. Separately, `core.ignorecase=true` means git keeps
tracking the old casing until a `git mv --force` records the rename.

### Phase 3 — Wiring ✅ done

Every orphan embedded in the page that should have it. **The library went from 70
of 144 files referenced (51% orphaned) to 185 of 185 — zero orphans, zero broken
references.**

Closed: C1–C3 (settings, ~50 images across three pages), C4, C5, D1–D9, A1–A5,
A7–A12, and every B-row. 14 files retired — the byte-identical duplicate, four
confirmed visual duplicates, the misnamed length-picker, two extra names for the
word-entry keyboard, the two casing typos, and four settings pickers whose attrs
no longer exist (`donate` and `io_test` are menu actions, not settings;
`show_xpub` was superseded by `xpub_details`).

`generate.py --links` now enforces both directions permanently. Orphan rot is
invisible unless something counts it, which is how the library reached 51%.

### Phase 4 — Prose reconciliation ✅ done

- Fingerprint `593c4724` → `b5aa2761`. Only one site existed, not the ~6 expected.
- Addresses and paths reconciled to testnet-primary with mainnet noted, across
  `first-wallet`, `receive`, `recover`, `xpub-export`, `address-explorer`.
- **SS-3** — Legacy and Custom Derivation now documented under all three
  script-type tables, with the Custom Derivation keypad shown.
- **X-3 / X-5** — `creation.md` repointed at the real length picker;
  `address-explorer.md` step 1 split into three properly-illustrated steps.
- **X-4** — `power.md` rewritten: the device shows "Just Unplug It", so there is
  no confirmation step and no shutdown state, and both power-off methods now
  correctly end by unplugging.
- **MS-1** — `receive.md` notes that its captures show the single-sig case.
- **D9** — `contribute/testnet.md` now shows the indicator it always claimed
  existed: green tSats, `tb1q…` prefixes, "(Testnet)" labels.

One prose claim was corrected against the rendered screen: the backup-quiz
mistake view names the *wrong* word chosen, not the expected one.

Ordering note: Phase 4 must land in the same commit as Phase 2, or the docs
briefly show mainnet prose beside testnet screenshots.

---

## Verification

Four checks, all runnable from `generate.py`:

```bash
python docs-screenshots/generate.py --out docs/images   # render + size asserts
python docs-screenshots/generate.py --census            # every file in one bucket
python docs-screenshots/generate.py --links             # refs resolve, none orphaned
```

1. **Generation-time asserts** — fails if a shot writes no file, if output is not
   240×240, or if two manifest entries claim the same filename.
2. **Census** — every file in `docs/images/` belongs to exactly one of
   GENERATED / PRESERVED / RETIRED. Catches a screen quietly dropped from the
   manifest.
3. **Link check** — both directions: every reference resolves, and every file is
   referenced.
4. **Visual read-back** — a human or agent opens the PNGs and reads the values.

The fourth is the one that cannot be automated and the one that matters most.
Every check above passes on a screenshot of the wrong menu row, which is exactly
what SS-1 was. During this work it caught three real defects that the automated
checks passed clean: the wrong settings row, a prose claim about the backup-quiz
error screen, and `ScriptTypeOptions.png` being a different View than assumed.

---

### Phase 5 — Coordinator screenshots ✅ done (Sparrow)

A6, A9, B10 and X-1's Sparrow half. **16 captures**, wiring the coordinator side
of `first-wallet`, `receive`, `send`, `multisig`, `recover`, `psbt-signing`,
`multisig/spending` and `multisig/descriptor`. Procedure and per-file inventory:
[docs-screenshots/COORDINATOR.md](docs-screenshots/COORDINATOR.md).

Sparrow Wallet 2.5.3, Testnet3, light theme, 1:1 pixels. The testnet decision paid
off exactly as predicted: both wallets are the canonical fixture, so the
coordinator screenshots and the device screenshots describe the same wallet.

Three things that make the set hold together:

- **Keys enter by output descriptor**, pasted into *Script Policy → Descriptor →
  Edit…*. Sparrow derives the fingerprints and paths itself, so `b5aa2761` /
  `m/84'/1'/0'` and the three msig fingerprints `f79a2f18 / 7b764b64 / 86442e23`
  are computed on screen, not typed.
- **The Receive tab was advanced to index 5**, so it shows
  `tb1qwp75hxqf7hx5qx2gvvekarhacvf9fx0mw7p4sl` — the same address
  `SeedAddressVerificationSuccessView.png` reports as verified. `receive.md`'s two
  halves now agree, which also settles SS-6 visually.
- **`send.md` shows the journey PSBT**, opened via *File → Open Transaction →
  From Text*. Sparrow identifies the signing wallet as My Single-Sig and the
  change output as 148,500 sats — the same numbers `PSBTMathView` renders. Its
  inputs are synthetic, so it is unbroadcastable by construction and the Broadcast
  button can be captured live with no risk.

`Sparrow_DescriptorQR.png` was decoded with pyzbar and carries the real fixture
descriptor with all three fingerprints — one coordinator capture that is
machine-verifiable rather than eyeballed.

Reading the real UI corrected four prose claims: SeedSigner offers **Scan…** only
(not "Import / Scan"), the policy option is **Multi Signature HD**, the network
switch is **Tools → Restart In → Testnet3**, and the keystore button is
**Watch Only Wallet**.

#### Still open

~~**No webcam on the capture machine.**~~ **Closed.** With a camera attached, both
keystore captures were re-shot from a real QR scan off the emulator
(`docs-screenshots/live_emulator.py` loads the four fixture seeds), so
`Type:` now reads **Airgapped Wallet (Seedsigner)** instead of "Watch Only
Wallet" and the crops start above that row. The scanned tpub matches the
descriptor-loaded one byte for byte, so no other capture moved.

The mid-scan webcam frame was captured too. Sparrow's two scan entry points —
*SeedSigner → Scan…* and *Signatures → Scan QR* — render the **same** dialog
(901 px differ outside the video area, all of it progress-bar animation), so one
file covers both steps.

~~**Still open: the viewports.**~~ **Closed.** Both the device-side camera frames
(X-2) and the Sparrow-side ones show a live feed that has to be composited by
hand, and all six now are. `docs-screenshots/camera_qrs.py` renders the QR
belonging in each, from the canonical fixture via SeedSigner's own encoders — so
a reader who decodes one gets the real address, PSBT or xpub.

| File | Viewport now shows |
|---|---|
| `AddressVerificationsCameraView.png` | the fixture receive address `tb1qwp75hxq…` |
| `SeedPSBTCameraView.png` | a frame of the unsigned journey PSBT |
| `Sparrow_ScanKeystoreQR.png` | `UR:CRYPTO-ACCOUNT/…` — the fixture xpub |
| `Sparrow_ScanSignedPSBT.png` | `UR:CRYPTO-PSBT/…` — the signed journey PSBT |

The two entropy frames (`SeedCameraEntropyView.png`, `SeedEntropyPreviewView.png`)
carry a photograph instead, since what they capture is a scene, not a code.

**BlueWallet is not covered.** `bluewallet.md` steps 2, 4 and 5 stay text-only —
it is a mobile app with no Windows build, so it needs a phone-capture session of
its own. A10/A11 concern the *device*-side BlueWallet screens and were already
closed in Phase 3.

**Not attempted: Sparrow's Send tab.** Composing a spend (recipient, amount, fee)
needs a funded wallet, and funding the fixture would produce a different
transaction from the one the device screenshots review. Continuity won; the
transaction view stands in for the compose step.

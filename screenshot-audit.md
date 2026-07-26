# Screenshot audit — SeedSigner docs

Read-only audit of `docs/images/` (144 files) against every markdown image
reference in `docs/`. No files were modified.

**Method.** Every `docs/get-started/*.md` and `docs/reference/**/*.md` page was
read step by step. Every screenshot embedded in a get-started journey was opened
and read visually (not inferred from filename), plus ~50 further images from
`docs/images/` for cross-checking and duplicate detection.

**Headline numbers**

| Metric | Value |
|---|---|
| Files in `docs/images/` | 144 |
| Distinct files actually referenced | 70 (+ `SeedSigner_Logo.png` from `index.html`) |
| **Orphaned (zero references)** | **74 — 51% of the library** |
| get-started journeys with **zero** screenshots | 3 of 7 (`send.md`, `multisig.md`, `bluewallet.md`) |
| Reference/help/security pages with zero screenshots | 25 of 34 |
| Coordinator-side (Sparrow/BlueWallet) screenshots in repo | 0 |

The dominant pattern: **the library is not the problem — the wiring is.** Most
gaps below can be closed by embedding an image that already exists.

---

## Part 1 — Missing screenshot inventory

### 1.1 Screenshot density per journey

| Journey | Steps | Screenshots | Ratio |
|---|---|---|---|
| `get-started/first-wallet.md` | 8 | 11 | good, but gaps at the highest-stakes sub-steps |
| `get-started/receive.md` | 3 | 5 | good |
| `get-started/build-device.md` | 11 | 1 | thin |
| `get-started/recover.md` | 4 | 1 | thin |
| `get-started/send.md` | 4 | **0** | **none** |
| `get-started/multisig.md` | 5 | **0** | **none** |
| `get-started/bluewallet.md` | 5 | **0** | **none** |

`receive.md` and `send.md` are presented as the two halves of "Everyday use"
(`get-started/README.md:16-19`). One has 5 screenshots for 3 steps; the other
has 0 for 4. That asymmetry is the clearest instance of the "sibling steps have
one, this one doesn't" problem.

### 1.2 HIGH — get-started

| # | Location | Missing screen | Why it matters | Image already exists? |
|---|---|---|---|---|
| A1 | `docs/get-started/send.md:40` (Step 3, "Review every detail, this is the important part") | The PSBT review screen — recipient, amount, fee, change | The page's own framing calls this "the whole reason to use a signer" (`send.md:24`) and warns transactions are irreversible (`send.md:51`). The reader is told to scrutinise a screen they have never been shown. Highest-severity gap in the audit. | **Yes** — `docs/images/PSBTOverviewView.png` |
| A2 | `docs/get-started/send.md:53-58` (Step 4, Approve) | Select Signer, then Sign PSBT / Approve | No visual confirmation before an irreversible action. | **Yes** — `PSBTSelectSeedView.png`, `PSBTFinalizeView.png` |
| A3 | `docs/get-started/send.md:36-38` (Step 2, Scan the PSBT) | Seed menu → Scan PSBT; camera view | Entry point of the whole journey. | **Yes** — `SeedMainMenuPSBTSelectView.png`, `SeedPSBTCameraView.png` |
| A4 | `docs/get-started/first-wallet.md:124` (Step 3, sub-step 5) | Xpub privacy warning ("Privacy Leak! / I Understand") | Sub-steps 1, 2, 3, 4 and 6 of the same list each have a screenshot; only 5 does not. Textbook mid-flow drop. | **Yes** — `SeedExportXpubWarningView.png` (used at `reference/keys/xpub-export.md:40`) |
| A5 | `docs/get-started/first-wallet.md:125-127` (Step 3, sub-step 6) | Xpub Details — fingerprint / derivation / xpub review | Jumps straight to the QR. This is the screen holding the fingerprint the reader is told to compare 22 lines later at `first-wallet.md:149`. | **Yes** — `SeedExportXpubDetailsView.png` (but see finding SS-4: it shows the wrong fingerprint) |
| A6 | `docs/get-started/first-wallet.md:139-152` (Step 4, all 9 sub-steps) | Sparrow: New Wallet, Policy Type, Script Type, Keystore → Airgapped Hardware Wallet, imported-keystore fingerprint | Entire coordinator half of the journey is text-only, including the fingerprint-comparison step (`:147-149`) that the recovery drill later depends on. | **No** — no coordinator screenshots exist anywhere in the repo |
| A7 | `docs/get-started/first-wallet.md:204-208` (Step 7, sign a spend) | Scan PSBT → review → Approve | Three sub-steps, no images, irreversible action. | **Yes** — same PSBT set as A1-A3 |
| A8 | `docs/get-started/multisig.md:62-68` (Step 3, "On SeedSigner", 7 sub-steps) | Network check, seed select, Export Xpub, **Multisig**, Native Segwit, Sparrow, Export Xpub | The whole device side of multisig setup is text-only, repeated three times by the reader. | **Partly** — but `SeedExportXpubSigTypeView.png` has **Single Sig** highlighted, so a new Multisig capture is required (see MS-2) |
| A9 | `docs/get-started/multisig.md:85-89` (Step 5, descriptor backup) | Sparrow File → Export Wallet → Specter Desktop → Show/Export | Marked "critical… without it, recovering your wallet may be impossible" (`multisig.md:87`). No visual at all, here or at `reference/multisig/descriptor.md`. | **No** |
| A10 | `docs/get-started/bluewallet.md:36` (Step 1, sub-step 1) | Settings → Coordinator Software, BlueWallet enabled | Zero-cost fix; two matching images sit orphaned. | **Yes** — `SettingsMainMenuCoordinatorSoftwareSelectView.png` and `SettingsEntryUpdateSelectionView_coordinators.png` (BlueWallet is the first row) |
| A11 | `docs/get-started/bluewallet.md:38` (Step 1, sub-step 3) | Coordinator selection with BlueWallet highlighted | The exact image exists and is currently mis-deployed in `first-wallet.md` where the prose says Sparrow. One move fixes A11 and SS-1 together. | **Yes** — `SeedExportXpubCoordinatorView.png` |
| A12 | `docs/get-started/build-device.md:77` (Step 8) | Splash screen, then the "you can remove the SD card" notice | The single moment a first-time builder cannot distinguish "booting" from "dead" — `reference/device/first-boot.md:15` warns the screen stays blank ~45 s. Step 9 immediately after *does* have a screenshot. | **No** — no splash or SD-notice capture exists |

### 1.3 MEDIUM — get-started

| # | Location | Missing screen | Image exists? |
|---|---|---|---|
| B1 | `first-wallet.md:73` (Step 1.2, "choose 24 words") | Mnemonic Length picker | **Yes** — `SeedMnemonicLengthCalcView.png` |
| B2 | `first-wallet.md:74` (Step 1.3, security warning) | "Caution / Classified Info! / I Understand" | **Yes** — `SeedWarningView.png` |
| B3 | `first-wallet.md:88` (Step 2.1, "Transcribe all words") | Seed words, four at a time | **Yes** — `SeedMnemonicEntryView.png`. The page shows the *quiz* (`:91`) but never the screen being quizzed. |
| B4 | `first-wallet.md:218-221` (Step 8, recovery drill, 4 sub-steps) | Discard Seed → confirm; Load a Seed; Finalize Seed | **Yes** — `DiscardSeedSelectView.png`, `DiscardSeedMainMenuView.png`, `LoadASeedMainMenuView.png`, `SeedFinalizeView.png` |
| B5 | `recover.md:34-35` (Step 1, both load paths) | Load A Seed menu, word entry, SeedQR scan | **Yes** — `LoadASeedMainOptionSelectView.png`, `LoadASeedMainMenuView.png`, `SeedWordEnterView.png`, `SeedQRScan.png`. Only 1 screenshot serves 4 steps on this page. |
| B6 | `recover.md:59` (Step 4, re-verify address) | Verify Address success | **Yes** — the 5-image set already used in `receive.md:41-57` |
| B7 | `multisig.md:31-37` (Step 1, create three seeds) | Any seed-creation screen | **Yes** — the `creation.md` set |
| B8 | `bluewallet.md:51-57` (Step 3, verify a receive address) | Address Explorer or Verify Address | **Yes** — existing verify set |
| B9 | `build-device.md:82` (Step 10, first-run setup) | Any of the four recommended settings screens | **Yes** — 51 orphaned settings images |
| B10 | `receive.md:33` (Step 1) | Coordinator Receive tab | **No** |

### 1.4 Reference pages — HIGH

Pages that describe many sub-screens or menu options and show **zero**:

| # | Page | Scope described | Orphaned images that cover it |
|---|---|---|---|
| C1 | `docs/reference/settings/advanced.md` | 16 settings, each with its own detail section (`:36-141`) | ~30: `BitcoinNetworkSelectView.png`, `QRCodeDensitySelectView.png`, `XPubExportSelectView.png`, `SigTypesSelectView.png`, `ScriptTypeSelectView.png`, `ShowXpubDetailsSelectView.png`, `BIP-39PassphraseSelectView.png`, `CameraRotationSelectView.png`, `CompactSeedQRSelectView.png`, `BIP-85ChildSeedsSelectView.png`, `ElectrumSeedsSelectView.png`, `MessageSigningSelectView.png`, `ShowPrivacyWarningsSelectView.png`, `ShowDireWarningsSelectView.png`, `ShowQrBrightnessTipsSelectVIew.png`, `ShowPartnerLogosSelectVIew.png` + the matching `SettingsEntryUpdateSelectionView_*` value pickers |
| C2 | `docs/reference/settings/basic.md` | 5 settings + 5 detail sections (`:13-66`) | `SettingsMainMenuCoordinatorSoftwareSelectView.png`, `…DenominationDisplaySelectView.png`, `…PersistentSelectView.png`, `…InputOutputSelectView.png`, `…DonateSelectView.png`, `…LanguageSelectView.png`, `…AdvancedSelectView.png` + `SettingsEntryUpdateSelectionView_{coordinators,denomination,persistent_settings,io_test,donate,locale}.png` |
| C3 | `docs/reference/settings/hardware.md` | 2 settings, 3 display drivers, a troubleshooting section (`:13-53`) | `HardwareSelectView.png`, `DisplayTypeSelectView.png`, `InvertColorsSelectView.png`, `SettingsEntryUpdateSelectionView_display_type.png`, `…_color_inverted.png` |
| C4 | `docs/help/error-messages.md:7` ("Unknown QR Type") | 3 named error screens | `ScanInvalidQRTypeView.png` **is literally that error screen** ("Error / Unknown QR Type / QRCode is invalid or is a data format not yet supported"). A page about recognising error messages shows none of them. |
| C5 | `docs/reference/seeds/loading.md:65-75` (BIP-39 passphrase) | Passphrase entry + the fingerprint-change concept | `SeedAddPassphraseView_{lowercase,uppercase,digits,symbols_1,symbols_2}.png` and `SeedPassphraseReviewView.png` — the latter shows "changes fingerprint 73c5da0a >> c1535941", exactly the concept `loading.md:67-71` explains in prose. |

### 1.5 Reference pages — MEDIUM / LOW

| # | Location | Gap | Image exists? |
|---|---|---|---|
| D1 | `docs/reference/seeds/creation.md:113-119` | The three final-word entropy options (coin flips / word selection / zeros) are listed but none shown | **Yes** — `ToolsCalcFinalWordCoinFlipsView.png`, `…CoinFlipResultView.png`, `…EntropyView.png`, `…EntropyResultView.png`, `…EnterSeedView.png`, `…DoneView.png` (all 6 orphaned) |
| D2 | `docs/reference/keys/message-signing.md` | 7-step flow, 0 images | Partly — `MessageSigningSelectView.png`, `SettingsEntryUpdateSelectionView_message_signing.png` (device screens for the flow itself do not exist) |
| D3 | `docs/reference/seeds/bip85.md:23-31` | 6-step derivation flow, 0 images | Partly — `BIP-85ChildSeedsSelectView.png`, `SettingsEntryUpdateSelectionView_bip85.png` |
| D4 | `docs/reference/multisig/spending.md` | 4-step two-signature flow, 0 images | Partly — PSBT set exists but is single-sig |
| D5 | `docs/reference/keys/address-explorer.md:13` | "choose your loaded seed" sub-step unillustrated | **Yes** — `SavedSeedSelectView.png`, `AddressExplorerSelectSourceView.png` |
| D6 | `docs/reference/device/navigation.md:34-36` | "power icon in the top-right corner" described, not shown | **Yes** — `PowerIconSelectedScreen.png` (Home with the power icon highlighted). Same gap at `reference/device/power.md:11` and `:32`. |
| D7 | `docs/reference/settings/settingsqr.md:22-25` | The post-scan confirmation screen the page tells you to review (`:36`) | **No** |
| D8 | `docs/reference/software/first-run.md:9-40` | 4 recommended settings screens, 0 images | **Yes** — orphaned settings set |
| D9 | `docs/contribute/testnet.md:53-56` | Network switch + the "visual indicator" the page claims the device displays | Partly — `BitcoinNetworkSelectView.png`, `SettingsEntryUpdateSelectionView_network.png` (but the latter shows **Mainnet** selected; no testnet-state capture exists anywhere) |
| D10 | `docs/reference/seeds/creation.md:86-87` | Dice method steps 6-7 (warning, backup verify) reference screens shown only in Method 1 | **Yes** — reuse `SeedWarningView.png`, `SeedBackupTestView.png` (low priority; de-duplication is defensible) |

---

## Part 2 — Mock-data consistency audit

### 2.1 Single-sig journey

Files: `build-device.md` → `first-wallet.md` → `receive.md` → `send.md` →
`recover.md` (+ `bluewallet.md`).

**Canonical values stated in prose**

| Value | Source | Stated as |
|---|---|---|
| Master fingerprint | `first-wallet.md:147` | `593c4724` ("a short code like") |
| Derivation path | `first-wallet.md:147`, `:225`, `:267`; `recover.md:55` | `m/84'/0'/0'` mainnet, `m/84'/1'/0'` testnet |
| Signature type | `first-wallet.md:106`, `:233`, `:260` | Single Sig |
| Script type | `first-wallet.md:110`, `:142`, `:233`, `:267` | Native SegWit / P2WPKH |
| Address prefix | `first-wallet.md:114`, `:152`; `receive.md:33` | `bc1q…` |
| Coordinator | `first-wallet.md:120`, `:140` | Sparrow, wallet named "My Single-Sig" |
| Seed length | `first-wallet.md:73` | 24 words |
| Network | `first-wallet.md:12` recommends testnet; every path/address given is mainnet | mixed |

**Values actually legible on the journey's screenshots** (all opened and read)

| Image | Embedded at | On-screen data | Verdict |
|---|---|---|---|
| `MainMenuView.png` | `build-device.md:80` | Home; Scan highlighted | no flow data — fine |
| `ToolsMenuView.png` | `first-wallet.md:78` | Tools; camera "New seed" highlighted | fine |
| `SeedBackupTestView.png` | `first-wallet.md:91` | "Verify Word #11" → off / high / sea / drastic | see SS-5 |
| `SeedExportXpubSigTypeView.png` | `first-wallet.md:108` | **Single Sig** highlighted | ✓ matches `:106` |
| `SeedExportXpubScriptTypeView.png` | `first-wallet.md:118` | Native Segwit highlighted; list = Native Segwit, Nested Segwit, **Legacy**, Taproot, **Custom Derivation** | ✓ selection; see SS-3 |
| `SeedExportXpubCoordinatorView.png` | `first-wallet.md:122` | **BlueWallet** highlighted; Sparrow unhighlighted, 3rd row | ✗ **SS-1** |
| `SeedExportXpubQRView.png` | `first-wallet.md:127` | QR only | no legible data — fine |
| `VerifyAddressSelectView.png` | `first-wallet.md:165`, `receive.md:41` | Tools; Verify Address highlighted | ✓ |
| `AddressVerificationsCameraView.png` | `first-wallet.md:169`, `receive.md:45` | blank black frame, "< back \| Scan address QR" | see X-3 |
| `AddressVerificationsMainMenuScreen.png` | `first-wallet.md:173`, `receive.md:49` | fingerprint **`593c4724`** | ✓ matches `:147` |
| `SeedAddressVerificationView.png` | `first-wallet.md:177`, `receive.md:53` | `bc1q6p0…q86f5ek`, "Single Sig - Native Segwit" | ✓ |
| `SeedAddressVerificationSuccessView.png` | `first-wallet.md:181`, `receive.md:57` | `bc1q6p0…q86f5ek`, "receive address index 5" | ✓ consistent with the previous image |
| `SeedFinalizeView.png` | `recover.md:39` | fingerprint **`8c65eb9f`** | ✗ **SS-2** |

#### SS-1 — HIGH — Coordinator screenshot contradicts the prose beside it

- `docs/get-started/first-wallet.md:120` — "4. Select **Sparrow** as the coordinator."
- `docs/images/SeedExportXpubCoordinatorView.png`, embedded at `first-wallet.md:122` — **BlueWallet** is the highlighted (orange) row. Sparrow is the third row, unselected.
- Compounding: `first-wallet.md:33`, `:140`, `:261` and the whole journey are Sparrow-based; `:262-265` repeat Sparrow in the quick-reference table.
- The same image at `reference/keys/xpub-export.md:36` is fine — that prose is generic ("Select your coordinator wallet software from the list").

**Fix:** re-shoot with Sparrow highlighted for `first-wallet.md`. Then reuse the
existing BlueWallet capture at `get-started/bluewallet.md:38`, whose prose does
say "select **BlueWallet** as the coordinator" and which currently has no
screenshot at all (gap A11).

#### SS-2 — HIGH — Recovery-drill fingerprint breaks the journey thread

- Journey fingerprint is `593c4724`: prose `first-wallet.md:147`, and on screen in `AddressVerificationsMainMenuScreen.png` (`first-wallet.md:173`, `receive.md:49`).
- `docs/get-started/recover.md:39` embeds `docs/images/SeedFinalizeView.png`, which shows **`8c65eb9f`**.
- The prose immediately below, `recover.md:45`: "**A matching fingerprint means you've reconstructed the same wallet.**" The illustration of a successful recovery shows a fingerprint that does not match the wallet the reader built. `first-wallet.md:220` makes the identical demand ("the seed fingerprint must equal the one Sparrow showed in Step 4").

**Fix:** shoot a new `SeedFinalizeView` at `593c4724` for `recover.md:39`. Save
it under a **new filename** — `SeedFinalizeView.png` is shared with
`reference/seeds/loading.md:35` and `:57`, which are standalone and can keep the
current capture.

#### SS-3 — MEDIUM — Script-type table omits two options the screenshot shows

- `first-wallet.md:113-116` tabulates three script types; `SeedExportXpubScriptTypeView.png` at `:118` shows **five** rows, including `Legacy` and `Custom Derivation`.
- Identical mismatch at `reference/keys/xpub-export.md:26-32` (table of 3) vs. the same image at `:32`.
- Reader-facing effect: two on-screen options are undocumented at the exact moment of choosing.

**Fix:** prose. Add one line under each table noting that Legacy and Custom
Derivation also appear and when to ignore them. (`SeedExportXpubCustomDerivationView.png`
— the "Derivation Path" keypad — is orphaned and would illustrate the latter.)

#### SS-4 — MEDIUM — The only fingerprint/derivation screen in the library shows a third value

- `docs/images/SeedExportXpubDetailsView.png` reads: Fingerprint `720d2d65`, Derivation `m/84'/0'/0'`, Xpub `zpub6rGMoUv5Ck4cs…`.
- It is referenced only from `reference/keys/xpub-export.md:44`, never from the journey — which is itself gap A5.
- Derivation `m/84'/0'/0'` ✓ matches `first-wallet.md:147`. The fingerprint `720d2d65` is a third distinct value (vs. `593c4724` in prose and `8c65eb9f` in `recover.md`).
- Corroborating SS-1: the `zpub…` prefix is the SLIP-132 P2WPKH serialisation used by BlueWallet/Electrum, not the `xpub…` Sparrow expects. Together with the BlueWallet-highlighted coordinator screen, this indicates the whole xpub-export series was captured in a BlueWallet session.

**Fix:** if this screen is added to `first-wallet.md` between `:124` and `:127`
(gap A5), it must be re-shot as `593c4724` / `m/84'/0'/0'` / `xpub…`.

#### SS-5 — LOW — Seed length: 24 in prose, evidence points at 12

- `first-wallet.md:73` — "choose **24 words**".
- `SeedBackupTestView.png` at `:91` shows "Verify Word #11". Not conclusive on its own (the quiz can pick word 11 of a 24-word seed), but the same file at `reference/seeds/creation.md:57` sits under a 12-word capture — `SeedMnemonicEntryView.png` (`creation.md:49`) reads "Seed Words: **1/3**", i.e. three pages of four = 12 words.
- Confidence: low. Flagged so that if B1/B3 are filled in, the new captures use a 24-word seed.

#### SS-6 — LOW — Verified address never appears in prose

`bc1q6p0…q86f5ek` / receive index 5 is internally consistent across
`SeedAddressVerificationView.png` and `SeedAddressVerificationSuccessView.png`,
but is stated nowhere in text. Recorded here as the canonical journey address so
a future edit does not introduce a second one.

#### SS-7 — LOW/MEDIUM — Testnet is recommended everywhere and shown nowhere

- `first-wallet.md:12`, `get-started/README.md:39`, `multisig.md:39` and `contribute/testnet.md:7` all push testnet-first practice.
- Every legible address across all 144 images is mainnet `bc1q…`; no `tb1q…` appears anywhere. `SettingsEntryUpdateSelectionView_network.png` shows **Mainnet** ticked.
- `contribute/testnet.md:56` asserts "The device displays a visual indicator so you always know which network you're on" — no screenshot of that indicator exists.
- Network mismatch is named the single most common failure mode (`first-wallet.md:244`, `:248`; `multisig.md:100`), yet the reader has no picture of what "on testnet" looks like.

### 2.2 Multisig journey

Files: `multisig.md`, which reuses `receive.md` and `send.md` for later steps.

**Canonical values stated in prose**

| Value | Source | Stated as |
|---|---|---|
| Policy | `multisig.md:3`, `:47`, `:108` | 2 of 3 |
| Signature type | `multisig.md:64`, `:108` | Multisig |
| Script type | `multisig.md:65`, `:108` | Native Segwit |
| Coordinator | `multisig.md:43`, `:66` | Sparrow, wallet named "My Multisig" |
| Keystores | `multisig.md:51`, `:74` | Keystore 1/2/3 → "SeedSigner 1/2/3" |
| Seeds | `multisig.md:37` | labelled Seed 1, Seed 2, Seed 3 |
| Fingerprints / addresses / amounts | — | **none stated** |

**Screenshots in `multisig.md`: none.** All findings below concern the pages it
hands the reader off to.

#### MS-1 — MEDIUM-HIGH — Multisig readers are sent to single-sig screenshots

- `multisig.md:116` — "[Receive bitcoin](/get-started/receive.md): **verify a multisig receive address** before sharing it."
- `docs/images/SeedAddressVerificationView.png`, embedded at `receive.md:53`, reads **"Single Sig - Native Segwit"** on screen.
- `receive.md:33` prose likewise: "**single-sig** Native SegWit addresses start with `bc1q…`".
- A reader following the multisig journey lands on a page whose only device screenshots explicitly say Single Sig.

**Fix:** either shoot a multisig variant of the verification pair, or add a
qualifier at `receive.md:33` and a note beside `receive.md:53` that the capture
shows the single-sig case.

#### MS-2 — MEDIUM — No Multisig-highlighted signature-type capture exists

- `multisig.md:64` — "4. Select **Multisig**."
- The library's only signature-type screen, `docs/images/SeedExportXpubSigTypeView.png`, has **Single Sig** highlighted, so gap A8 cannot be closed by reuse. A new capture is required.

#### MS-3 — LOW — The one orphaned multisig screen shows the wrong quorum

- `docs/images/AddressExplorerAddressTypeView.png` (orphaned) reads "Wallet descriptor / **1 / 2 multisig**".
- It is the only multisig-specific device screenshot in the repo, but its policy contradicts the 2-of-3 the journey teaches (`multisig.md:3`, `:47`). If it is ever pulled into `multisig.md`, it needs re-shooting as 2-of-3.

### 2.3 Cross-cutting — affects both journeys

#### X-1 — MEDIUM — No coordinator-side screenshots exist at all

All 144 files in `docs/images/` are device screens or hardware photos. Every
Sparrow/BlueWallet instruction is text-only:
`first-wallet.md:139-152`, `:206-208`; `multisig.md:43-47`, `:53-58`, `:78-82`;
`recover.md:52`; `receive.md:33`; `send.md:34`, `:57-58`;
`bluewallet.md:45-47`, `:65-66`, `:73`; `reference/multisig/descriptor.md:36-45`.
Roughly half of every journey is unillustrated as a direct consequence.

#### X-2 — MEDIUM — Three "camera view" screenshots are blank black frames

| Image | Used at | What it shows |
|---|---|---|
| `AddressVerificationsCameraView.png` | `first-wallet.md:169`, `receive.md:45` | black frame + "< back \| Scan address QR" |
| `SeedPSBTCameraView.png` | `reference/keys/psbt-signing.md:22` | black frame + "< back \| Scan PSBT" |
| `SeedCameraEntropyView.png` | `reference/seeds/creation.md:33` | black frame + "< back \| click a button" — captioned "Camera viewfinder capturing environmental entropy", showing no viewfinder content |

`docs/images/SeedQRScan.png` (`reference/seeds/loading.md:53`) proves a
viewfinder capture *with* a code visible in frame is achievable, so these three
are re-shootable. (`SeedQRCameraView.png` is a fourth blank frame, orphaned.)

#### X-3 — MEDIUM — Wrong screenshot for the step

`docs/reference/seeds/creation.md:41` embeds `docs/images/SeedMnemonicLengthView.png`
with alt text "Seed length selection showing 12-word and 24-word options", under
prose reading "5. Choose **12 words** or **24 words**."

The image is **not** a length picker — it is the **Seed Word #1 keyboard**
("h" typed, `habit` highlighted in the suggestion list). The genuine screen is
`docs/images/SeedMnemonicLengthCalcView.png` ("Mnemonic Length / 12 words /
24 words"), already used at `creation.md:103`. `SeedMnemonicLengthView.png` is
misnamed and mis-deployed.

**Fix:** point `creation.md:41` at `SeedMnemonicLengthCalcView.png`; rename or
retire `SeedMnemonicLengthView.png`.

#### X-4 — MEDIUM — Screenshot contradicts the step it illustrates

`docs/reference/device/power.md:18` embeds `docs/images/PowerOffView.png` with
alt text "Power off confirmation screen", between:

- `:16` — "3. Select **Power Off**."
- `:20` — "4. Confirm when prompted. The device shuts down."

The image actually reads "**Just Unplug It** — It is safe to disconnect power at
any time." There is no confirmation and no shutdown; the device instructs the
user to pull the cable. The prose describes a flow the device does not have.

**Fix:** rewrite `power.md:20` to match the screen, or re-shoot if a confirmation
screen exists in current firmware.

#### X-5 — LOW — Mislabelled image in Address Explorer

`docs/reference/keys/address-explorer.md:15` embeds
`docs/images/SeedOptionSelectView.png` with alt text "Select seed". The image is
the **Home screen with Seeds highlighted** — no seed is being selected. The
actual seed-selection screens (`SavedSeedSelectView.png` "In-Memory Seeds", and
`AddressExplorerSelectSourceView.png`) are both orphaned. See gap D5.

#### X-6 — LOW — Capture resolution is inconsistent across the library

59 files are clean 240×240 device captures. The rest split into hand-cropped
232–241 px captures and a second series at ~290–298 px. Pages mix both, so image
size visibly jumps while scrolling — e.g. `reference/seeds/loading.md` runs
296×297 (`:17`), 298×294 (`:21`), 296×298 (`:29`), then 240×240 (`:35`).

---

## Part 3 — Orphaned and duplicate image files

### 3.1 Orphans — 74 files, 51% of `docs/images/`

Every file below has **zero** markdown or HTML references anywhere in `docs/`.
Grouped by the page that ought to use them, so this list doubles as the
work-queue for Part 1.

**Group A — settings screens (51 files).** Two parallel, complementary
conventions: `<Setting>SelectView.png` = the menu with that row highlighted;
`SettingsEntryUpdateSelectionView_<setting>.png` = that setting's value picker.
Together they form a complete navigate-then-choose pair for every documented
setting. `docs/reference/settings/{basic,advanced,hardware}.md` use **none** of
them (findings C1–C3).

- Menu rows (27): `SettingsMainMenu{AdvancedSelectView, CoordinatorSoftwareSelectView, DenominationDisplaySelectView, DonateSelectView, InputOutputSelectView, LanguageSelectView, PersistentSelectView}.png`; `BIP-39PassphraseSelectView.png`, `BIP-85ChildSeedsSelectView.png`, `BitcoinNetworkSelectView.png`, `CameraRotationSelectView.png`, `CompactSeedQRSelectView.png`, `DisplayTypeSelectView.png`, `ElectrumSeedsSelectView.png`, `HardwareSelectView.png`, `HomeScreenSettingsSelectView.png`, `InvertColorsSelectView.png`, `MessageSigningSelectView.png`, `QRCodeDensitySelectView.png`, `ScriptTypeSelectView.png`, `ShowDireWarningsSelectView.png`, `ShowPartnerLogosSelectVIew.png`, `ShowPrivacyWarningsSelectView.png`, `ShowQrBrightnessTipsSelectVIew.png`, `ShowXpubDetailsSelectView.png`, `SigTypesSelectView.png`, `XPubExportSelectView.png`
- Value pickers (24): `SettingsEntryUpdateSelectionView_{bip85, camera_rotation, color_inverted, compact_seedqr, coordinators, denomination, display_type, donate, electrum_seeds, io_test, locale, message_signing, network, partner_logos, passphrase, persistent_settings, privacy_warnings, qr_brightness_tips, qr_density, script_types, show_xpub, sig_types, xpub_details, xpub_export}.png`

**Group B — BIP-39 passphrase (6 files)** → `reference/seeds/loading.md:65-75` (finding C5)
`SeedAddPassphraseView_{lowercase,uppercase,digits,symbols_1,symbols_2}.png`, `SeedPassphraseReviewView.png`

**Group C — calculate-final-word (6 files)** → `reference/seeds/creation.md:113-119` (finding D1)
`ToolsCalcFinalWord{CoinFlipsView, CoinFlipResultView, EntropyView, EntropyResultView, EnterSeedView, DoneView}.png`

**Group D — seed / address selection (7 files)**
`SavedSeedSelectView.png`, `AddressExplorerSelectSourceView.png` → D5 · `AddressExplorerAddressTypeView.png` → MS-3 · `SeedMenuAddressExplorerSelectView.png` → near-dup, §3.2 · `SeedExportXpubCustomDerivationView.png` → SS-3 · `SeedTranscribeSeedQRDoneSelectView.png` → near-dup, §3.2 · `SeedQRCameraView.png` → blank frame, X-2

**Group E — misc (4 files)**
`ScanInvalidQRTypeView.png` → C4 (highest-value single orphan) · `PowerIconSelectedScreen.png` → D6 · `HomeScreenToolsSelectView.png` → near-dup, §3.2 · `SeedFinalizeView copy.png` → delete, §3.2

### 3.2 Duplicates and near-duplicates

| Confidence | Files | Evidence | Recommendation |
|---|---|---|---|
| **High — byte-identical** | `docs/images/SeedFinalizeView copy.png` and `docs/images/SeedFinalizeView.png` | Identical MD5 `6910c42dc12603890ee83bab72bdd701`, both 9,971 bytes, both show fingerprint `8c65eb9f` | Delete the ` copy.png`. Only the canonical name is referenced (`reference/seeds/loading.md:35`, `:57`; `get-started/recover.md:39`). |
| **High — visually identical** | `HomeScreenToolsSelectView.png` (237×237, orphan) vs `ToolsOptionSelectView.png` (237×238, used at `reference/seeds/creation.md:25`) | Both opened: same Home screen, Tools tile highlighted, no visible difference | Delete the orphan, or standardise on one filename. |
| **High — visually identical** | `SeedMenuAddressExplorerSelectView.png` (238×238, orphan) vs `AddressExplorerSelectView.png` (237×237, used at `reference/keys/address-explorer.md:17`) | Both opened: same seed menu, fingerprint `73c5da0a`, Address Explorer highlighted | Delete the orphan. |
| **Medium — same screen, two scales, both in use** | `SeedOptionSelectView.png` (238×233, `reference/keys/address-explorer.md:15`) vs `SeedsOptionSelectView.png` (297×296, `reference/seeds/loading.md:15`) | Both opened: Home screen, Seeds tile highlighted | Consolidate on one; contributes to X-6. Note `SeedOptionSelectView.png` is also mislabelled (X-5). |
| **Low — deliberate variant** | `SeedTranscribeSeedQRConfirmQRPromptView.png` (Confirm highlighted, `reference/seeds/seedqr.md:39`) vs `SeedTranscribeSeedQRDoneSelectView.png` (Done highlighted, orphan) | Same screen, different selection | Keep both only if `seedqr.md:41-42` illustrates each branch; otherwise retire the orphan. |
| **Low — superseded** | `SeedQRCameraView.png` (orphan, blank frame) vs `SeedQRScan.png` (`reference/seeds/loading.md:53`, QR visible in frame) | Same camera screen; the used one is strictly better | Delete the orphan. |

### 3.3 Other file-level notes

- **Not a broken link:** the reference scan reports `images/filename.png` as unresolved. It comes from the syntax example at `docs/contribute/docs.md:170` and is intentional.
- **Filename typos** in the orphan set: `ShowPartnerLogosSelectVIew.png` and `ShowQrBrightnessTipsSelectVIew.png` (capital `I` in "VIew"). Worth fixing before they are wired up.
- **Non-screenshot assets, all correctly referenced:** `SeedSigner_Device_and_Components.jpg` (`docs/README.md:7`), `WaveShare_LCD_Hat.png` (`reference/device/navigation.md:7`), `SeedSigner_Logo.png` (`docs/index.html:722`), `docs/favicon-32x32.png` (outside `images/`).

---

## Suggested order of work

1. **`send.md`** — embed the five existing PSBT screenshots (A1–A3). Highest impact, zero new captures, closes the irreversible-action gap.
2. **`SeedFinalizeView copy.png`** — delete (§3.2). One line of cleanup.
3. **Two mis-deployed images** — repoint `creation.md:41` (X-3) and move the BlueWallet coordinator capture from `first-wallet.md:122` to `bluewallet.md:38` (SS-1 + A11).
4. **Settings pages** — wire up Group A orphans into `settings/{basic,advanced,hardware}.md` (C1–C3); 51 images, no new captures.
5. **`ScanInvalidQRTypeView.png` → `help/error-messages.md:7`** (C4). One image, one line.
6. **Re-shoots** — Sparrow-highlighted coordinator (SS-1), `593c4724` Finalize Seed for `recover.md` (SS-2), Multisig sig-type (MS-2), the three blank camera frames (X-2).
7. **`multisig.md` and `bluewallet.md`** — currently zero screenshots each (A8–A11).
8. **Coordinator-side captures** — the largest new-work item (X-1); needed before `first-wallet.md` Step 4 and `multisig.md` Steps 2/4/5 can be illustrated.

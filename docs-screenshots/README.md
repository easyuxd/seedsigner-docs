# docs-screenshots

Generates the device screenshots in `docs/images/` from code, so every capture is
reproducible and every on-screen value matches the prose beside it.

Three kinds of image live in the library. Most are **generated** headlessly from
the manifest. A handful are **preserved** because nothing headless can produce
them — the coordinator GUI ([COORDINATOR.md](COORDINATOR.md)) and the live camera
frames, whose viewports are composited by hand from QRs built by
[camera_qrs.py](camera_qrs.py). `--census` enforces that every file is in exactly
one bucket.

See [../screenshot-regen-plan.md](../screenshot-regen-plan.md) for why this
exists and [../screenshot-audit.md](../screenshot-audit.md) for the gaps it
closes.

## Running it

Needs the [SeedSigner emulator](https://github.com/enteropositivo/seedsigner-emulator)
checkout and its venv. Assumed to sit beside this repo as
`../seedsigner-emulator/seedsigner-app`; override with `$env:SEEDSIGNER_APP`.

```bash
../seedsigner-emulator/seedsigner-app/src/.venv/Scripts/python.exe docs-screenshots/generate.py
```

Output goes to `docs-screenshots/out/` (gitignored). Writing into the live
library is an explicit choice:

```bash
python docs-screenshots/generate.py --out docs/images
```

Render a single screen while iterating (`--only` takes one substring):

```bash
python docs-screenshots/generate.py --only Coordinator
```

Checks:

```bash
python docs-screenshots/generate.py --census
```

Every file in `docs/images/` must belong to exactly one of GENERATED (in the
manifest), PRESERVED (cannot be rendered headlessly), or RETIRED (to delete).
Catches a screen quietly dropped from the manifest.

```bash
python docs-screenshots/generate.py --links
```

Every image reference resolves, **and** every image file is referenced. The
second direction is the one that rots — the audit found 51% of the library
orphaned, which stays invisible unless something counts it.

```bash
python docs-screenshots/generate.py --retire
```

Deletes the RETIRED files. The one destructive step, so it is separate. It skips
any name that differs from a generated filename only by letter case: on Windows
and macOS those are the same file, and deleting the old name would delete the
newly rendered content.

## Layout

| File | Role |
|---|---|
| `shim.py` | Bootstrap: Pi hardware mocks, app on `sys.path`, the `run_screen` patch, the `Shot` dataclass |
| `fixture.py` | The canonical seed, addresses, descriptor, network — all derived from fixed entropy |
| `manifest.py` | Every screen: which View, what kwargs, what output filename |
| `generate.py` | Driver and verification |
| `live_emulator.py` | Launches the **running** emulator with the fixture seeds loaded — for anything needing a real camera |
| `camera_qrs.py` | Renders the QRs composited into the camera viewports, from the fixture via SeedSigner's own encoders |
| `COORDINATOR.md` | How the hand-captured `Sparrow_*.png` screens were shot, and how to redo them |

Nothing here edits the emulator checkout. The app is imported read-only and the
upstream `ScreenshotRenderer` is loaded by file path, so emulator upgrades cannot
clobber this pipeline.

## Adding a screen

```python
Shot(
    seed_views.SeedExportXpubCoordinatorView,
    dict(seed_num=0, sig_type="ss", script_type="nat"),
    filename="SeedExportXpubCoordinatorView.png",
    screen_kwargs=highlight("Sparrow"),
    note="audit SS-1",
)
```

- **`filename`** is independent of the View name on purpose. Existing docs
  filenames survive upstream View renames, so the markdown does not churn.
- **`highlight("...")`** captures a menu with that row selected. Prefer it over a
  raw `selected_button` index — indices drift when upstream reorders a menu, and
  a stale index renders a plausible screenshot of the wrong row. A label that
  does not match, or matches ambiguously, raises instead.
- **`run_before`** mutates the `Controller` for screens that need data loaded
  first.

## Verifying

`generate.py` fails the run if a shot writes no file or the output is not
240×240. That catches absence and size, not content.

**Content still needs a human or an agent to look at the PNG.** Wrong-but-plausible
screenshots are the failure mode this whole effort exists to fix: the audit's SS-1
(BlueWallet highlighted where the prose said Sparrow) would pass every automated
check here. Open the regenerated images and read the values.

## The fixture

Testnet only. The mnemonics are published in a public repo and must never hold
value. Entropy comes from fixed tag strings, so the fixture is rebuildable from
`fixture.py` alone — there is no secret to lose, and the values quoted in the
prose can always be re-derived and re-checked.

One seed carries the whole single-sig journey, three siblings carry the 2-of-3
multisig, and `build_psbt()` produces an unsigned testnet spend from that same
wallet so the `send.md` review screens show the reader's own transaction.

```bash
python -c "import sys; sys.path.insert(0,'docs-screenshots'); import fixture; print(fixture.summary())"
```

"""Launch the SeedSigner emulator with the docs fixture already loaded.

The headless pipeline in this directory renders screens that need no hardware.
The camera views (audit X-2) are the exception: they show a live webcam frame, so
they can only be captured from the *running* emulator with a real camera.

    python docs-screenshots/live_emulator.py

Press ``S`` (or F12) in the emulator window to save a 240x240 PNG into
``seedsigner-app/seedsigner-screenshots/live/``.

Deliberately does **not** import ``shim`` or ``fixture``: ``shim`` mocks
``seedsigner.hardware.camera`` and the displays, which is the opposite of what a
live capture session needs. The mnemonics are re-derived here from the same fixed
tags, and asserted against the fingerprints the docs quote, so the two paths
cannot silently drift apart.
"""

import hashlib
import os
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_DEFAULT_APP = REPO_ROOT.parent / "seedsigner-emulator" / "seedsigner-app"
APP_ROOT = pathlib.Path(os.environ.get("SEEDSIGNER_APP") or _DEFAULT_APP)
APP_SRC = APP_ROOT / "src"

if not (APP_SRC / "seedsigner").is_dir():
    raise SystemExit(f"SeedSigner app not found at {APP_ROOT}")

sys.path.insert(0, str(APP_SRC))
# The emulator resolves settings.json and its live-screenshot directory relative
# to src/, so run from there exactly as run-emulator.ps1 does.
os.chdir(APP_SRC)

from embit import bip39  # noqa: E402

from seedsigner.controller import Controller  # noqa: E402
from seedsigner.models.seed import Seed  # noqa: E402
from seedsigner.models.settings_definition import SettingsConstants  # noqa: E402

_TAG = "seedsigner-docs canonical fixture v1"

# Every fingerprint the docs quote. If a seed here stopped matching, the camera
# captures would silently disagree with every other screenshot in the library.
EXPECTED = ["b5aa2761", "f79a2f18", "7b764b64", "86442e23"]


def _mnemonic(tag: str) -> list[str]:
    return bip39.mnemonic_from_bytes(hashlib.sha256(tag.encode()).digest()).split()


def main() -> None:
    controller = Controller.get_instance()
    settings = controller.settings

    settings.set_value(SettingsConstants.SETTING__NETWORK, SettingsConstants.TESTNET)
    settings.set_value(SettingsConstants.SETTING__SIG_TYPES,
                       [attr for attr, _ in SettingsConstants.ALL_SIG_TYPES])
    settings.set_value(SettingsConstants.SETTING__SCRIPT_TYPES,
                       [attr for attr, _ in SettingsConstants.ALL_SCRIPT_TYPES])
    settings.set_value(SettingsConstants.SETTING__COORDINATORS,
                       [attr for attr, _ in SettingsConstants.ALL_COORDINATORS])

    mnemonics = [_mnemonic(_TAG)] + [_mnemonic(f"{_TAG} msig {i}") for i in (1, 2, 3)]
    for mnemonic in mnemonics:
        controller.storage.seeds.append(Seed(
            mnemonic=mnemonic,
            wordlist_language_code=SettingsConstants.WORDLIST_LANGUAGE__ENGLISH,
        ))

    fingerprints = [s.get_fingerprint(SettingsConstants.TESTNET)
                    for s in controller.storage.seeds]
    if fingerprints != EXPECTED:
        raise SystemExit(f"fixture drift: got {fingerprints}, expected {EXPECTED}")

    print(f"Loaded seeds: {' / '.join(fingerprints)}  (testnet)")
    print("Press S or F12 in the emulator window to save a 240x240 screenshot.")
    controller.start()


if __name__ == "__main__":
    main()

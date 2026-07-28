"""Bootstrap for the docs screenshot pipeline.

Import this before anything else touches ``seedsigner.*``. It installs the
Raspberry Pi hardware mocks that the real modules would otherwise fail on, so
importing this module has side effects by design.

Nothing here edits the emulator checkout. The app is put on ``sys.path`` and its
``ScreenshotRenderer`` is loaded straight from the file, so emulator upgrades
cannot clobber the docs pipeline and the docs pipeline cannot corrupt the
emulator.
"""

import dataclasses
import importlib.util
import os
import pathlib
import sys
from contextlib import contextmanager
from typing import Any, Callable, Optional
from unittest.mock import MagicMock, patch

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

_DEFAULT_APP = REPO_ROOT.parent / "seedsigner-emulator" / "seedsigner-app"
APP_ROOT = pathlib.Path(os.environ.get("SEEDSIGNER_APP") or _DEFAULT_APP)
APP_SRC = APP_ROOT / "src"

if not (APP_SRC / "seedsigner").is_dir():
    raise SystemExit(
        f"SeedSigner app not found at {APP_ROOT}\n"
        "Point SEEDSIGNER_APP at the seedsigner-app directory of your emulator "
        "checkout, e.g.\n"
        '  $env:SEEDSIGNER_APP = "C:\\path\\to\\seedsigner-emulator\\seedsigner-app"'
    )

sys.path.insert(0, str(APP_SRC))

# Must precede any seedsigner import: these modules touch Pi-only hardware.
for _name in (
    "seedsigner.hardware.displays.st7789_mpy",
    "seedsigner.hardware.displays.ili9341",
    "seedsigner.views.screensaver.ScreensaverScreen",
    "RPi",
    "RPi.GPIO",
    "seedsigner.hardware.camera",
    "seedsigner.hardware.microsd",
):
    sys.modules[_name] = MagicMock()

# Match the Pi Zero's text rendering, which has no libraqm.
patch("PIL.ImageFont.core.HAVE_RAQM", False).start()


def _load_upstream_utils():
    """Load the emulator's screenshot utils by path.

    ``tests/`` is not a package, so a normal import would depend on pytest's
    rootdir handling. Loading the file directly keeps this independent of pytest.
    """
    path = APP_ROOT / "tests" / "screenshot_generator" / "utils.py"
    if not path.is_file():
        raise SystemExit(f"Upstream screenshot utils missing: {path}")
    spec = importlib.util.spec_from_file_location("ss_docs_screenshot_utils", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_utils = _load_upstream_utils()
ScreenshotRenderer = _utils.ScreenshotRenderer
ScreenshotComplete = _utils.ScreenshotComplete

CANVAS_SIZE = (240, 240)


@dataclasses.dataclass
class Shot:
    """One screenshot.

    ``filename`` is the name written into the output directory and is the only
    thing the markdown ever sees, so existing docs filenames can be preserved
    even when upstream renames the View.

    ``screen_kwargs`` are merged into the Screen the View builds — this is how
    "menu row N highlighted" states are captured without driving the GUI.
    """

    View_cls: Any
    view_kwargs: Optional[dict] = None
    filename: Optional[str] = None
    screen_kwargs: Optional[dict] = None
    screen_mutate: Optional[Callable] = None
    toast: Optional[Callable] = None  # zero-arg factory returning a toast thread
    run_before: Optional[Callable] = None
    run_after: Optional[Callable] = None
    note: str = ""

    def __post_init__(self):
        self.view_kwargs = dict(self.view_kwargs or {})
        self.screen_kwargs = dict(self.screen_kwargs or {})
        if not self.filename:
            self.filename = f"{self.View_cls.__name__}.png"
        if not self.filename.endswith(".png"):
            self.filename += ".png"


_current_screen_kwargs: dict = {}
_current_mutator: Optional[Callable] = None


def install_run_screen_patch():
    """Route every Screen construction through our overrides.

    ``View.run_screen`` is the single choke point every View uses to build its
    Screen, so one patch covers every screen in the app. This reimplements its
    two-line body (``views/view.py:112``) rather than delegating, so a mutator
    can run between construction and display.
    """
    from seedsigner.views.view import View

    def run_screen(self, Screen_cls, **kwargs):
        if _current_screen_kwargs:
            overrides = dict(_current_screen_kwargs)
            label = overrides.pop(SELECT_LABEL, None)
            if label is not None:
                overrides["selected_button"] = _row_index_for_label(kwargs, label)
            _reject_unknown_kwargs(Screen_cls, overrides)
            kwargs = {**kwargs, **overrides}

        self.screen = Screen_cls(**kwargs)
        if _current_mutator:
            # For state that lives on a component rather than a Screen field --
            # e.g. TopNav.is_selected, which highlights the power icon.
            _current_mutator(self.screen)
        return self.screen.display()

    View.run_screen = run_screen


SELECT_LABEL = "select_label"


def _row_index_for_label(screen_kwargs: dict, label: str) -> int:
    """Resolve a menu row by its visible text.

    Row indices drift whenever upstream reorders a menu, and a stale index
    renders a plausible-looking screenshot of the wrong row -- silent, and only
    catchable by eye. Matching on the label makes that failure loud instead.
    """
    button_data = screen_kwargs.get("button_data") or []
    labels = [getattr(b, "button_label", str(b)) for b in button_data]
    if label in labels:
        return labels.index(label)

    matches = [i for i, text in enumerate(labels) if label.lower() in text.lower()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(
            f"select_label {label!r} is ambiguous: matches {[labels[i] for i in matches]}"
        )
    raise ValueError(f"select_label {label!r} not found. Rows are: {labels}")


def _reject_unknown_kwargs(Screen_cls, overrides):
    """Fail loudly on a typo instead of silently rendering the default state.

    A silently-ignored ``selected_button`` would produce a plausible-looking but
    wrong screenshot, which is exactly the class of bug the audit had to catch
    by eye.
    """
    if not dataclasses.is_dataclass(Screen_cls):
        return
    known = {f.name for f in dataclasses.fields(Screen_cls)}
    unknown = set(overrides) - known
    if unknown:
        raise TypeError(
            f"{Screen_cls.__name__} has no field(s) {sorted(unknown)}. "
            f"Available: {sorted(known)}"
        )


@contextmanager
def screen_overrides(overrides: Optional[dict], mutator: Optional[Callable] = None):
    global _current_screen_kwargs, _current_mutator
    _current_screen_kwargs = dict(overrides or {})
    _current_mutator = mutator
    try:
        yield
    finally:
        _current_screen_kwargs = {}
        _current_mutator = None


def select_power_icon(screen):
    """Highlight the top-right power icon and clear any selected tile.

    `TopNav.is_selected` drives the icon; the tiles have to be cleared
    separately or the screenshot shows two things selected at once.
    """
    screen.top_nav.is_selected = True
    for button in getattr(screen, "buttons", []):
        button.is_selected = False

"""Which screens to render, and what filename each one gets.

Every file in `docs/images/` falls into exactly one of three buckets:

  GENERATED  -- in SHOTS below; rebuilt from the fixture on every run.
  PRESERVED  -- cannot be rendered headless (live camera frames, animated QR
                displays, hardware photos). The existing file is kept as-is.
  RETIRED    -- duplicate, misnamed, or superseded. Deleted, with any markdown
                reference repointed at the replacement.

`generate.py --census` reconciles those three against the directory so nothing
is silently dropped.

`filename` is deliberately independent of the View name: existing docs filenames
survive upstream View renames, so the markdown does not churn.
"""

import shim  # noqa: F401  -- must precede every seedsigner import

import fixture

from seedsigner.controller import Controller
from seedsigner.gui.screens.seed_screens import SeedAddPassphraseScreen
from seedsigner.gui.toast import (RemoveSDCardToastManagerThread,
                                  SDCardStateChangeToastManagerThread)
from seedsigner.hardware.microsd import MicroSD
from seedsigner.models.decode_qr import DecodeQR
from seedsigner.models.psbt_parser import PSBTParser
from seedsigner.models.qr_type import QRType
from seedsigner.models.seed import Seed
from seedsigner.models.settings_definition import SettingsConstants, SettingsDefinition
from seedsigner.views import (MainMenuView, NotYetImplementedView, PowerOptionsView,
                              RestartView, UnhandledExceptionView, psbt_views,
                              scan_views, seed_views, settings_views, tools_views)
from seedsigner.views.screensaver import OpeningSplashView
from seedsigner.views.view import NetworkMismatchErrorView, OptionDisabledView, PowerOffView

from shim import Shot, select_power_icon


def highlight(label: str) -> dict:
    """Highlight the menu row whose visible text is `label`.

    Prefer this over a raw `selected_button` index: indices drift when upstream
    reorders a menu, and the resulting screenshot looks fine while showing the
    wrong row.
    """
    return {shim.SELECT_LABEL: label}


def row(index: int) -> dict:
    """Highlight by index. Only for menus with duplicate labels.

    `ToolsMenuView` has two rows both reading "New seed" (image entropy and dice),
    so no label can distinguish them.
    """
    return {"selected_button": index}


# ---------------------------------------------------------------------------
# Per-shot state
#
# Every shot starts from the same baseline so the manifest can be reordered or
# filtered freely. Upstream's generator is order-dependent -- its
# ToolsAddressExplorerAddressTypeView only works because an earlier entry
# happened to leave a descriptor in the Controller -- and that is a bug class
# worth designing out.
# ---------------------------------------------------------------------------

def reset_state():
    """Restore the default single-sig journey state. Called before every shot."""
    controller = Controller.get_instance()
    settings = controller.settings

    settings.set_value(SettingsConstants.SETTING__NETWORK, fixture.NETWORK)
    settings.set_value(SettingsConstants.SETTING__SIG_TYPES,
                       [attr for attr, _ in SettingsConstants.ALL_SIG_TYPES])
    settings.set_value(SettingsConstants.SETTING__SCRIPT_TYPES,
                       [attr for attr, _ in SettingsConstants.ALL_SCRIPT_TYPES])
    settings.set_value(SettingsConstants.SETTING__COMPACT_SEEDQR,
                       SettingsConstants.OPTION__ENABLED)

    # The journey has one seed. Showing the multisig cosigners alongside it would
    # make every single-sig seed menu misleading.
    controller.storage.seeds.clear()
    controller.storage.seeds.append(fixture.SEED)
    controller.storage.set_pending_seed(fixture.SEED)

    controller.multisig_wallet_descriptor = None
    controller.resume_main_flow = None
    controller.address_explorer_data = None
    controller.psbt = None
    controller.psbt_seed = None
    controller.psbt_parser = None
    controller.unverified_address = fixture.address_verification_data()

    derivation = f"{fixture.SINGLE_SIG_DERIVATION}/0/0"
    from seedsigner.helpers import embit_utils
    controller.sign_message_data = {
        "seed_num": 0,
        "derivation_path": derivation,
        "message": "I attest that I control this bitcoin address",
        "addr_format": embit_utils.parse_derivation_path(derivation),
    }


def setup(controller):
    """One-time setup; per-shot state lives in reset_state()."""
    reset_state()


# --- state helpers used as run_before callbacks -----------------------------

def use_multisig_seeds():
    """Swap the journey seed for the three 2-of-3 cosigners."""
    storage = Controller.get_instance().storage
    storage.seeds.clear()
    for seed in fixture.MSIG_SEEDS:
        storage.seeds.append(seed)
    storage.set_pending_seed(fixture.MSIG_SEEDS[0])


def load_multisig_descriptor():
    from embit.descriptor import Descriptor

    Controller.get_instance().multisig_wallet_descriptor = Descriptor.from_string(
        fixture.MULTISIG_DESCRIPTOR
    )


def use_multisig_wallet():
    use_multisig_seeds()
    load_multisig_descriptor()


def load_psbt():
    controller = Controller.get_instance()
    decoder = DecodeQR()
    decoder.add_data(fixture.PSBT_BASE64)
    controller.psbt = decoder.get_psbt()
    controller.psbt_seed = fixture.SEED
    controller.psbt_parser = PSBTParser(p=controller.psbt, seed=fixture.SEED,
                                        network=fixture.NETWORK)


def load_psbt_awaiting_seed():
    """PSBTSelectSeedView only renders while no signing seed is chosen."""
    load_psbt()
    Controller.get_instance().psbt_seed = None


def load_multisig_psbt():
    use_multisig_wallet()
    controller = Controller.get_instance()
    decoder = DecodeQR()
    decoder.add_data(fixture.MULTISIG_PSBT_BASE64)
    controller.psbt = decoder.get_psbt()
    controller.psbt_seed = fixture.MSIG_SEEDS[0]
    controller.psbt_parser = PSBTParser(p=controller.psbt, seed=fixture.MSIG_SEEDS[0],
                                       network=fixture.NETWORK)


def use_passphrase_seed():
    """A pending seed carrying a passphrase, for the review screen."""
    seed = Seed(mnemonic=fixture.MNEMONIC,
                passphrase="docs-PASSPHRASE*1",
                wordlist_language_code=SettingsConstants.WORDLIST_LANGUAGE__ENGLISH)
    Controller.get_instance().storage.set_pending_seed(seed)


def init_pending_mnemonic():
    """11 known words plus a placeholder, for the calc-final-word flow.

    The 12th word is deliberately not a valid checksum -- that is the state the
    user is in while the device is still calculating it.
    """
    storage = Controller.get_instance().storage
    storage.init_pending_mnemonic(num_words=12)
    for i, word in enumerate(fixture.MNEMONIC_12[:11]):
        storage.update_pending_mnemonic(word=word, index=i)
    storage.update_pending_mnemonic(word="satoshi", index=11)


def complete_pending_mnemonic():
    """A fully valid 12-word pending mnemonic.

    ToolsCalcFinalWordDoneView reports the finished seed's fingerprint, and
    `get_pending_mnemonic_fingerprint()` returns None on a bad checksum -- which
    the Done screen cannot render.
    """
    storage = Controller.get_instance().storage
    storage.init_pending_mnemonic(num_words=12)
    for i, word in enumerate(fixture.MNEMONIC_12):
        storage.update_pending_mnemonic(word=word, index=i)


def use_address_explorer_seed():
    """Populate `address_explorer_data` the way the app itself does.

    The address-list Views read state that AddressTypeView's constructor sets, so
    running that constructor is both the least duplicated and the most faithful
    way to set it up.
    """
    controller = Controller.get_instance()
    controller.resume_main_flow = Controller.FLOW__ADDRESS_EXPLORER
    tools_views.ToolsAddressExplorerAddressTypeView(
        seed_num=0, script_type=SettingsConstants.NATIVE_SEGWIT
    )


def use_address_explorer_flow():
    """Only the flow flag -- retitles the script-type screen 'Address Explorer'."""
    Controller.get_instance().resume_main_flow = Controller.FLOW__ADDRESS_EXPLORER


def use_mainnet():
    Controller.get_instance().settings.set_value(
        SettingsConstants.SETTING__NETWORK, SettingsConstants.MAINNET
    )


# ---------------------------------------------------------------------------
# Files that cannot be generated headlessly -- the existing captures are kept.
# ---------------------------------------------------------------------------

PRESERVED = {
    # Live camera frames. The renderer has no video source; upstream's generator
    # carries the same limitation ("Screenshot can't render live preview screens").
    # Audit X-2 wants three of these re-shot with a QR visible in frame.
    "AddressVerificationsCameraView.png": "live camera frame (audit X-2)",
    "SeedPSBTCameraView.png": "live camera frame (audit X-2)",
    "SeedCameraEntropyView.png": "live camera frame (audit X-2)",
    "SeedEntropyPreviewView.png": "captured entropy image",
    "SeedQRScan.png": "camera frame with a QR in view; the X-2 quality target",

    # Animated QR displays cycle frames; upstream leaves them out for the same
    # reason (see the commented-out SeedExportXpubQRDisplayView entry).
    "SeedExportXpubQRView.png": "animated QR display",
    "AddressExplorerQRView.png": "animated QR display",

    # Not device screens.
    "SeedSigner_Device_and_Components.jpg": "hardware photo",
    "SeedSigner_Logo.png": "brand asset",
    "WaveShare_LCD_Hat.png": "hardware photo",
}

# ---------------------------------------------------------------------------
# Files to delete, and what any reference to them should point at instead.
# ---------------------------------------------------------------------------

RETIRED = {
    "SeedFinalizeView copy.png": (
        None, "byte-identical duplicate of SeedFinalizeView.png (audit 3.2)"),
    "SeedMnemonicLengthView.png": (
        "SeedMnemonicLengthCalcView.png",
        "not a length picker -- it is the word-entry keyboard (audit X-3)"),
    "SeedOptionSelectView.png": (
        "SeedsOptionSelectView.png",
        "same Home screen at a second scale; also mislabelled (audit X-5, 3.2)"),
    "HomeScreenToolsSelectView.png": (
        "ToolsOptionSelectView.png", "visually identical duplicate (audit 3.2)"),
    "SeedMenuAddressExplorerSelectView.png": (
        "AddressExplorerSelectView.png", "visually identical duplicate (audit 3.2)"),
    "SeedQRCameraView.png": (
        "SeedQRScan.png", "blank frame superseded by a capture with a QR (audit 3.2)"),
    "WordEntry.png": (
        "SeedMnemonicEntryView.png", "third filename for the word-entry keyboard"),
    "SeedWordEnterView.png": (
        "SeedMnemonicEntryView.png", "second filename for the word-entry keyboard"),
    "ShowPartnerLogosSelectVIew.png": (
        "ShowPartnerLogosSelectView.png", "filename typo: VIew (audit 3.3)"),
    "ShowQrBrightnessTipsSelectVIew.png": (
        "ShowQrBrightnessTipsSelectView.png", "filename typo: VIew (audit 3.3)"),
    "ToolsCalcFinalWordEntropyResultView.png": (
        "ToolsCalcFinalWordShowFinalWordView.png",
        "same Final Word Calc screen under a second name"),

    # These settings no longer exist. Donate and I/O test are menu actions rather
    # than settings, and show_xpub was superseded by the xpub_details attr, whose
    # own picker capture is already in the library.
    "SettingsEntryUpdateSelectionView_donate.png": (
        None, "no such setting; Donate is a menu action (DonateView)"),
    "SettingsEntryUpdateSelectionView_io_test.png": (
        None, "no such setting; I/O test is a menu action (IOTestView)"),
    "SettingsEntryUpdateSelectionView_show_xpub.png": (
        "SettingsEntryUpdateSelectionView_xpub_details.png",
        "attr renamed to xpub_details, whose picker is already captured"),
}


# ---------------------------------------------------------------------------
# Settings screens
#
# Two complementary conventions, 51 files, none of them currently referenced
# (audit C1-C3):
#   <Setting>SelectView.png                        the menu with that row highlighted
#   SettingsEntryUpdateSelectionView_<attr>.png    that setting's value picker
# ---------------------------------------------------------------------------

GENERAL = SettingsConstants.VISIBILITY__GENERAL
ADVANCED = SettingsConstants.VISIBILITY__ADVANCED
HARDWARE = SettingsConstants.VISIBILITY__HARDWARE

# Payloads for the SettingsQR ingest screens. Testnet, matching the fixture.
_QR_COMMON = ("coords=spa,spd denom=thr network=T qr_density=M xpub_export=E "
              "sigs=ss,ms scripts=nat xpub_details=E passphrase=E camera=0 "
              "compact_seedqr=E bip85=D priv_warn=E dire_warn=E partners=E locale=en")
SETTINGS_QR_PERSISTENT = f"settings::v1 name=Docs_persistent persistent=E {_QR_COMMON}"
SETTINGS_QR_EPHEMERAL = f"settings::v1 name=Docs_ephemeral persistent=D {_QR_COMMON}"

# (filename, menu visibility, row label) -- labels verified against rendered output.
SETTINGS_MENU_ROWS = [
    ("SettingsMainMenuLanguageSelectView.png", GENERAL, "Language"),
    ("SettingsMainMenuPersistentSelectView.png", GENERAL, "Persistent settings"),
    ("SettingsMainMenuCoordinatorSoftwareSelectView.png", GENERAL, "Coordinator software"),
    ("SettingsMainMenuDenominationDisplaySelectView.png", GENERAL, "Denomination display"),
    ("SettingsMainMenuAdvancedSelectView.png", GENERAL, "Advanced"),
    ("SettingsMainMenuInputOutputSelectView.png", GENERAL, "I/O test"),
    ("SettingsMainMenuDonateSelectView.png", GENERAL, "Donate"),

    ("BitcoinNetworkSelectView.png", ADVANCED, "Bitcoin network"),
    ("QRCodeDensitySelectView.png", ADVANCED, "QR code density"),
    ("XPubExportSelectView.png", ADVANCED, "Xpub export"),
    ("SigTypesSelectView.png", ADVANCED, "Sig types"),
    ("ScriptTypeSelectView.png", ADVANCED, "Script types"),
    ("ShowXpubDetailsSelectView.png", ADVANCED, "Show xpub details"),
    ("BIP-39PassphraseSelectView.png", ADVANCED, "BIP-39 passphrase"),
    ("CameraRotationSelectView.png", ADVANCED, "Camera rotation"),
    ("CompactSeedQRSelectView.png", ADVANCED, "Compact SeedQR"),
    ("BIP-85ChildSeedsSelectView.png", ADVANCED, "BIP-85 child seeds"),
    ("ElectrumSeedsSelectView.png", ADVANCED, "Electrum seeds"),
    ("MessageSigningSelectView.png", ADVANCED, "Message signing"),
    ("ShowPrivacyWarningsSelectView.png", ADVANCED, "Show privacy warnings"),
    ("ShowDireWarningsSelectView.png", ADVANCED, "Show dire warnings"),
    ("ShowQrBrightnessTipsSelectView.png", ADVANCED, "Show QR brightness tips"),
    ("ShowPartnerLogosSelectView.png", ADVANCED, "Show partner logos"),
    ("HardwareSelectView.png", ADVANCED, "Hardware"),

    ("DisplayTypeSelectView.png", HARDWARE, "Display type"),
    ("InvertColorsSelectView.png", HARDWARE, "Invert colors"),
]


def _settings_menu_shots():
    shots = []
    for filename, visibility, label in SETTINGS_MENU_ROWS:
        kwargs = {} if visibility == GENERAL else dict(visibility=visibility)
        shots.append(Shot(settings_views.SettingsMenuView, kwargs,
                          filename=filename, screen_kwargs=highlight(label),
                          note="audit C1-C3"))
    # The three menus themselves, unhighlighted.
    shots += [
        Shot(settings_views.SettingsMenuView, filename="SettingsMenuView.png"),
        Shot(settings_views.SettingsMenuView, dict(visibility=ADVANCED),
             filename="SettingsMenuView__Advanced.png"),
        Shot(settings_views.SettingsMenuView, dict(visibility=HARDWARE),
             filename="SettingsMenuView__Hardware.png"),
    ]
    return shots


# Settings attr names drifted after the docs images were captured. Keeping the
# established filenames avoids renaming files the audit refers to by name.
PICKER_FILENAME_OVERRIDES = {
    "bip85_child_seeds": "SettingsEntryUpdateSelectionView_bip85.png",
    "display_config": "SettingsEntryUpdateSelectionView_display_type.png",
}


def _settings_value_picker_shots():
    """One value picker per setting, driven off SettingsDefinition itself."""
    shots = []
    for entry in SettingsDefinition.settings_entries:
        if entry.visibility not in (GENERAL, ADVANCED, HARDWARE):
            continue
        if entry.attr_name == SettingsConstants.SETTING__LOCALE:
            shots.append(Shot(settings_views.LocaleSelectionView,
                              filename="SettingsEntryUpdateSelectionView_locale.png",
                              note="locale has its own View"))
            continue
        filename = PICKER_FILENAME_OVERRIDES.get(
            entry.attr_name,
            f"SettingsEntryUpdateSelectionView_{entry.attr_name}.png",
        )
        shots.append(Shot(
            settings_views.SettingsEntryUpdateSelectionView,
            dict(attr_name=entry.attr_name),
            filename=filename,
            note="audit C1-C3",
        ))
    return shots


# ---------------------------------------------------------------------------
# The manifest
# ---------------------------------------------------------------------------

SHOTS = [
    # ===== Home, power, boot =====
    Shot(OpeningSplashView, dict(is_screenshot_renderer=True, force_partner_logos=True),
         filename="OpeningSplashView.png",
         note="audit A12 -- the splash build-device.md never showed"),
    Shot(OpeningSplashView, dict(is_screenshot_renderer=True, force_partner_logos=False),
         filename="OpeningSplashView_no_partner_logos.png"),
    Shot(MainMenuView, filename="MainMenuView.png"),
    Shot(MainMenuView, filename="MainMenuView_RemoveSDCardToast.png",
         toast=lambda: RemoveSDCardToastManagerThread(activation_delay=0, duration=0),
         note="audit A12 -- the 'you can remove the SD card' notice on first boot"),
    Shot(MainMenuView, filename="MainMenuView_SDCardStateChangeToast_inserted.png",
         toast=lambda: SDCardStateChangeToastManagerThread(
             action=MicroSD.ACTION__INSERTED, activation_delay=0, duration=0)),
    Shot(MainMenuView, filename="MainMenuView_SDCardStateChangeToast_removed.png",
         toast=lambda: SDCardStateChangeToastManagerThread(
             action=MicroSD.ACTION__REMOVED, activation_delay=0, duration=0)),
    Shot(MainMenuView, filename="SeedsOptionSelectView.png",
         screen_kwargs=highlight("Seeds")),
    Shot(MainMenuView, filename="ToolsOptionSelectView.png",
         screen_kwargs=highlight("Tools")),
    Shot(MainMenuView, filename="HomeScreenSettingsSelectView.png",
         screen_kwargs=highlight("Settings")),
    Shot(MainMenuView, filename="PowerIconSelectedScreen.png",
         screen_mutate=select_power_icon,
         note="audit D6 -- navigation.md and power.md describe this icon, never show it"),
    Shot(PowerOptionsView, filename="PowerOptionsView.png"),
    Shot(RestartView, filename="RestartView.png"),
    Shot(PowerOffView, filename="PowerOffView.png",
         note="audit X-4 -- reads 'Just Unplug It'; power.md prose must match"),

    # ===== Seed loading =====
    Shot(seed_views.SeedsMenuView, filename="SavedSeedSelectView.png",
         screen_kwargs=highlight(fixture.FINGERPRINT), note="audit D5"),
    Shot(seed_views.SeedsMenuView, filename="LoadASeedMainOptionSelectView.png",
         screen_kwargs=highlight("Load a seed")),
    Shot(seed_views.LoadSeedView, filename="LoadASeedMainMenuView.png"),
    # Two letters, not the default one: the matches panel only renders once
    # len(letters) > 1 (seed_screens.py:82), so the default "a" shows a bare
    # keyboard and hides the feature every page describing this screen leads
    # with. "ap" is the fixture's own first word, and lands on the 2-3 letters
    # the prose promises.
    Shot(seed_views.SeedMnemonicEntryView, filename="SeedMnemonicEntryView.png",
         screen_kwargs=dict(initial_letters=["a", "p"]),
         note="audit B3 -- also replaces WordEntry.png and SeedWordEnterView.png"),
    Shot(seed_views.SeedMnemonicInvalidView, filename="SeedMnemonicInvalidView.png"),
    Shot(seed_views.SeedFinalizeView, filename="SeedFinalizeView.png"),
    Shot(seed_views.SeedFinalizeView, filename="SeedFinalizeView_journey.png",
         note="audit SS-2 -- recover.md needs the journey fingerprint"),
    Shot(seed_views.SeedElectrumMnemonicStartView,
         filename="SeedElectrumMnemonicStartView.png"),

    # ===== BIP-39 passphrase (audit C5) =====
    Shot(seed_views.SeedAddPassphraseView, filename="SeedAddPassphraseView_lowercase.png"),
    Shot(seed_views.SeedAddPassphraseView,
         dict(initial_keyboard=SeedAddPassphraseScreen.KEYBOARD__UPPERCASE_BUTTON_TEXT),
         filename="SeedAddPassphraseView_uppercase.png"),
    Shot(seed_views.SeedAddPassphraseView,
         dict(initial_keyboard=SeedAddPassphraseScreen.KEYBOARD__DIGITS_BUTTON_TEXT),
         filename="SeedAddPassphraseView_digits.png"),
    Shot(seed_views.SeedAddPassphraseView,
         dict(initial_keyboard=SeedAddPassphraseScreen.KEYBOARD__SYMBOLS_1_BUTTON_TEXT),
         filename="SeedAddPassphraseView_symbols_1.png"),
    Shot(seed_views.SeedAddPassphraseView,
         dict(initial_keyboard=SeedAddPassphraseScreen.KEYBOARD__SYMBOLS_2_BUTTON_TEXT),
         filename="SeedAddPassphraseView_symbols_2.png"),
    Shot(seed_views.SeedAddPassphraseExitDialogView,
         filename="SeedAddPassphraseExitDialogView.png"),
    Shot(seed_views.SeedReviewPassphraseView, filename="SeedPassphraseReviewView.png",
         run_before=use_passphrase_seed,
         note="audit C5 -- shows the fingerprint change loading.md explains in prose"),

    # ===== Seed menu and backup =====
    Shot(seed_views.SeedOptionsView, dict(seed_num=0), filename="SeedOptionsView.png"),
    Shot(seed_views.SeedOptionsView, dict(seed_num=0), filename="SeedMenuView.png",
         screen_kwargs=highlight("Export Xpub")),
    Shot(seed_views.SeedOptionsView, dict(seed_num=0),
         filename="SeedMainMenuPSBTSelectView.png", screen_kwargs=highlight("Scan PSBT"),
         note="audit A3 -- entry point of the send.md journey"),
    Shot(seed_views.SeedOptionsView, dict(seed_num=0),
         filename="AddressExplorerSelectView.png",
         screen_kwargs=highlight("Address Explorer")),
    Shot(seed_views.SeedOptionsView, dict(seed_num=0),
         filename="BackupSeedSelectView.png", screen_kwargs=highlight("Backup Seed")),
    Shot(seed_views.SeedOptionsView, dict(seed_num=0),
         filename="DiscardSeedSelectView.png", screen_kwargs=highlight("Discard Seed")),
    Shot(seed_views.SeedBackupView, dict(seed_num=0),
         filename="ViewSeedWordsSelectView.png",
         screen_kwargs=highlight("View Seed Words")),
    Shot(seed_views.SeedBackupView, dict(seed_num=0),
         filename="ExportAsSeedQRSelectView.png",
         screen_kwargs=highlight("Export as SeedQR")),
    Shot(seed_views.SeedDiscardView, dict(seed_num=0),
         filename="DiscardSeedMainMenuView.png"),

    # ===== Viewing and verifying seed words =====
    Shot(seed_views.SeedWordsWarningView, dict(seed_num=0),
         filename="SeedWarningView.png", note="audit B2"),
    Shot(seed_views.SeedWordsWarningView, dict(seed_num=0),
         filename="ViewSeedWordsWarningView.png"),
    Shot(seed_views.SeedWordsView, dict(seed_num=0), filename="SeedWordsView.png"),
    Shot(seed_views.SeedWordsView, dict(seed_num=0, page_index=2),
         filename="SeedWordsView_2.png"),
    Shot(seed_views.SeedWordsBackupTestPromptView, dict(seed_num=0),
         filename="SeedWordsBackupTestPromptView.png"),
    Shot(seed_views.SeedWordsBackupTestView, dict(seed_num=0, rand_seed=6102),
         filename="SeedBackupTestView.png",
         note="upstream renamed the View; the docs filename is kept"),
    Shot(seed_views.SeedWordsBackupTestMistakeView,
         dict(seed_num=0, cur_index=7, wrong_word="satoshi"),
         filename="SeedWordsBackupTestMistakeView.png"),
    Shot(seed_views.SeedWordsBackupTestSuccessView, dict(seed_num=0),
         filename="SeedWordsBackupTestSuccessView.png"),

    # ===== SeedQR transcription =====
    Shot(seed_views.SeedTranscribeSeedQRFormatView, dict(seed_num=0),
         filename="SeedTranscribeSeedQRFormatView.png"),
    Shot(seed_views.SeedTranscribeSeedQRWarningView, dict(seed_num=0),
         filename="SeedTranscribeSeedQRWarningView.png"),
    Shot(seed_views.SeedTranscribeSeedQRWholeQRView,
         dict(seed_num=0, seedqr_format=QRType.SEED__SEEDQR, num_modules=29),
         filename="SeedTranscribeSeedQRWholeQRView_24_Standard.png"),
    Shot(seed_views.SeedTranscribeSeedQRWholeQRView,
         dict(seed_num=0, seedqr_format=QRType.SEED__COMPACTSEEDQR, num_modules=25),
         filename="SeedTranscribeSeedQRWholeQRView_24_Compact.png"),
    Shot(seed_views.SeedTranscribeSeedQRZoomedInView,
         dict(seed_num=0, seedqr_format=QRType.SEED__SEEDQR,
              initial_zone_x=2, initial_zone_y=2),
         filename="SeedTranscribeSeedQRZoomedInView_12_Standard.png",
         note="docs filename retained; the fixture seed is 24 words"),
    Shot(seed_views.SeedTranscribeSeedQRWholeQRView,
         dict(seed_num=0, seedqr_format=QRType.SEED__SEEDQR, num_modules=29),
         filename="SeedTranscribeSeedQRWholeQRView_12_Standard.png",
         note="docs filename retained"),
    Shot(seed_views.SeedTranscribeSeedQRConfirmQRPromptView, dict(seed_num=0),
         filename="SeedTranscribeSeedQRConfirmQRPromptView.png"),
    Shot(seed_views.SeedTranscribeSeedQRConfirmQRPromptView, dict(seed_num=0),
         filename="SeedTranscribeSeedQRDoneSelectView.png",
         screen_kwargs=highlight("Done")),
    Shot(seed_views.SeedTranscribeSeedQRConfirmWrongSeedView,
         filename="SeedTranscribeSeedQRConfirmWrongSeedView.png"),
    Shot(seed_views.SeedTranscribeSeedQRConfirmInvalidQRView,
         filename="SeedTranscribeSeedQRConfirmInvalidQRView.png"),
    Shot(seed_views.SeedTranscribeSeedQRConfirmSuccessView, dict(seed_num=0),
         filename="SeedTranscribeSeedQRConfirmSuccessView.png"),

    # ===== Xpub export =====
    Shot(seed_views.SeedExportXpubSigTypeView, dict(seed_num=0),
         filename="SeedExportXpubSigTypeView.png",
         screen_kwargs=highlight("Single Sig")),
    Shot(seed_views.SeedExportXpubSigTypeView, dict(seed_num=0),
         filename="SeedExportXpubSigTypeView_multisig.png",
         screen_kwargs=highlight("Multisig"), note="audit MS-2"),
    Shot(seed_views.SeedExportXpubScriptTypeView, dict(seed_num=0, sig_type="ss"),
         filename="SeedExportXpubScriptTypeView.png",
         screen_kwargs=highlight("Native Segwit"),
         note="audit SS-3 -- five rows; the prose tables list three"),
    Shot(seed_views.SeedExportXpubCustomDerivationView,
         dict(seed_num=0, sig_type="ss", script_type=""),
         filename="SeedExportXpubCustomDerivationView.png", note="audit SS-3"),
    Shot(seed_views.SeedExportXpubCoordinatorView,
         dict(seed_num=0, sig_type="ss", script_type="nat"),
         filename="SeedExportXpubCoordinatorView.png",
         screen_kwargs=highlight("Sparrow"),
         note="audit SS-1 -- first-wallet.md prose says Sparrow"),
    Shot(seed_views.SeedExportXpubCoordinatorView,
         dict(seed_num=0, sig_type="ss", script_type="nat"),
         filename="SeedExportXpubCoordinatorView_bluewallet.png",
         screen_kwargs=highlight("BlueWallet"), note="audit A11"),
    Shot(seed_views.SeedExportXpubWarningView,
         dict(seed_num=0, sig_type="ss", script_type="nat", coordinator="spa",
              custom_derivation=""),
         filename="SeedExportXpubWarningView.png", note="audit A4"),
    Shot(seed_views.SeedExportXpubDetailsView,
         dict(seed_num=0, sig_type="ss", script_type="nat", coordinator="spa",
              custom_derivation=""),
         filename="SeedExportXpubDetailsView.png", note="audit A5, SS-4"),

    # ===== Address verification =====
    Shot(seed_views.SeedSelectSeedView,
         dict(flow=Controller.FLOW__VERIFY_SINGLESIG_ADDR),
         filename="AddressVerificationsMainMenuScreen.png"),
    Shot(seed_views.AddressVerificationSigTypeView,
         filename="AddressVerificationSigTypeView.png"),
    Shot(seed_views.SeedAddressVerificationView, dict(seed_num=0),
         filename="SeedAddressVerificationView.png"),
    Shot(seed_views.SeedAddressVerificationSuccessView, dict(seed_num=0),
         filename="SeedAddressVerificationSuccessView.png"),

    # ===== Multisig (audit MS-1, MS-3, D4) =====
    Shot(seed_views.LoadMultisigWalletDescriptorView,
         filename="LoadMultisigWalletDescriptorView.png"),
    Shot(seed_views.MultisigWalletDescriptorView,
         filename="MultisigWalletDescriptorView.png", run_before=use_multisig_wallet,
         note="audit A9 -- descriptor backup, called critical and never shown"),

    # ===== Message signing (audit D2) =====
    Shot(seed_views.SeedSelectSeedView, dict(flow=Controller.FLOW__SIGN_MESSAGE),
         filename="SeedSelectSeedView_sign_message.png"),
    Shot(seed_views.SeedSignMessageConfirmMessageView,
         filename="SeedSignMessageConfirmMessageView.png"),
    Shot(seed_views.SeedSignMessageConfirmAddressView,
         filename="SeedSignMessageConfirmAddressView.png"),

    # ===== BIP-85 (audit D3) =====
    Shot(seed_views.SeedBIP85ApplicationModeView, dict(seed_num=0),
         filename="SeedBIP85ApplicationModeView.png"),
    Shot(seed_views.SeedBIP85SelectChildIndexView, dict(seed_num=0, num_words=24),
         filename="SeedBIP85SelectChildIndexView.png"),
    Shot(seed_views.SeedBIP85InvalidChildIndexView, dict(seed_num=0, num_words=12),
         filename="SeedBIP85InvalidChildIndexView.png"),

    # ===== PSBT signing: the send.md journey (audit A1-A3, A7) =====
    Shot(psbt_views.PSBTSelectSeedView, filename="PSBTSelectSeedView.png",
         run_before=load_psbt_awaiting_seed, note="audit A2 -- Select Signer"),
    Shot(psbt_views.PSBTOverviewView, filename="PSBTOverviewView.png",
         run_before=load_psbt,
         note="audit A1 -- the review screen send.md tells the reader to scrutinise"),
    Shot(psbt_views.PSBTMathView, filename="PSBTMathView.png", run_before=load_psbt),
    Shot(psbt_views.PSBTAddressDetailsView, dict(address_num=0),
         filename="PSBTAddressDetailsView.png", run_before=load_psbt),
    Shot(psbt_views.PSBTChangeDetailsView, dict(change_address_num=0),
         filename="PSBTChangeDetailsView.png", run_before=load_psbt),
    Shot(psbt_views.PSBTFinalizeView, filename="PSBTFinalizeView.png",
         run_before=load_psbt, note="audit A2 -- Approve"),
    Shot(psbt_views.PSBTNoChangeWarningView, filename="PSBTNoChangeWarningView.png"),
    Shot(psbt_views.PSBTUnsupportedScriptTypeWarningView,
         filename="PSBTUnsupportedScriptTypeWarningView.png"),
    Shot(psbt_views.PSBTSigningErrorView, filename="PSBTSigningErrorView.png",
         run_before=load_psbt),
    Shot(psbt_views.PSBTAddressVerificationFailedView,
         dict(is_change=True, is_multisig=False),
         filename="PSBTAddressVerificationFailedView_singlesig_change.png"),
    Shot(psbt_views.PSBTAddressVerificationFailedView,
         dict(is_change=False, is_multisig=False),
         filename="PSBTAddressVerificationFailedView_singlesig_selftransfer.png"),
    Shot(psbt_views.PSBTAddressVerificationFailedView,
         dict(is_change=True, is_multisig=True),
         filename="PSBTAddressVerificationFailedView_multisig_change.png"),
    Shot(psbt_views.PSBTAddressVerificationFailedView,
         dict(is_change=False, is_multisig=True),
         filename="PSBTAddressVerificationFailedView_multisig_selftransfer.png"),

    # Multisig spend (audit D4)
    Shot(psbt_views.PSBTOverviewView, filename="PSBTOverviewView_multisig.png",
         run_before=load_multisig_psbt, note="audit D4"),
    Shot(psbt_views.PSBTChangeDetailsView, dict(change_address_num=0),
         filename="PSBTChangeDetailsView_multisig_verified.png",
         run_before=load_multisig_psbt),

    # ===== Tools =====
    Shot(tools_views.ToolsMenuView, filename="ToolsMenuView.png"),
    Shot(tools_views.ToolsMenuView, filename="SeedGenerateCalcMethodView.png",
         screen_kwargs=highlight("Calc 12th/24th word")),
    Shot(tools_views.ToolsMenuView, filename="SeedGenerateDiceMethodView.png",
         screen_kwargs=row(1), note="two rows read 'New seed'; index is unavoidable"),
    Shot(tools_views.ToolsMenuView, filename="VerifyAddressSelectView.png",
         screen_kwargs=highlight("Verify Address")),
    Shot(tools_views.ToolsImageEntropyMnemonicLengthView,
         filename="SeedMnemonicLengthCalcView.png",
         note="audit B1, X-3 -- the genuine length picker"),
    Shot(tools_views.ToolsDiceEntropyMnemonicLengthView,
         filename="SeedMnemonicLengthDiceView.png"),
    Shot(tools_views.ToolsDiceEntropyEntryView, dict(total_rolls=50),
         filename="ToolsDiceEntropyEntryView.png"),
    Shot(tools_views.ToolsDiceEntropyEntryView, dict(total_rolls=99),
         filename="ToolsDiceEntropyProgressView.png"),

    # Calculate final word (audit D1)
    Shot(tools_views.ToolsCalcFinalWordNumWordsView,
         filename="ToolsCalcFinalWordNumWordsView.png"),
    Shot(tools_views.ToolsCalcFinalWordCoinFlipsView,
         filename="ToolsCalcFinalWordCoinFlipsView.png", run_before=init_pending_mnemonic),
    Shot(tools_views.ToolsCalcFinalWordShowFinalWordView,
         filename="ToolsCalcFinalWordShowFinalWordView.png",
         run_before=init_pending_mnemonic),
    Shot(tools_views.ToolsCalcFinalWordShowFinalWordView, dict(coin_flips="0010101"),
         filename="ToolsCalcFinalWordCoinFlipResultView.png",
         run_before=init_pending_mnemonic),
    Shot(tools_views.ToolsCalcFinalWordFinalizePromptView,
         filename="ToolsCalcFinalWordFinalizePromptView.png",
         run_before=init_pending_mnemonic),
    Shot(tools_views.ToolsCalcFinalWordDoneView,
         filename="ToolsCalcFinalWordDoneView.png",
         run_before=complete_pending_mnemonic),
    Shot(seed_views.SeedMnemonicEntryView, dict(cur_word_index=0),
         filename="ToolsCalcFinalWordEnterSeedView.png",
         run_before=init_pending_mnemonic, note="audit D1 -- entering the known words"),
    Shot(seed_views.SeedMnemonicEntryView,
         dict(cur_word_index=11, is_calc_final_word=True),
         filename="ToolsCalcFinalWordEntropyView.png",
         run_before=init_pending_mnemonic,
         note="audit D1 -- word-selection entropy method, the 12th word"),

    # Address Explorer (audit D5)
    Shot(tools_views.ToolsAddressExplorerSelectSourceView,
         filename="AddressExplorerSelectSourceView.png", note="audit D5"),
    # The script-type picker is SeedExportXpubScriptTypeView retitled: it reads
    # "Address Explorer" when resume_main_flow is the explorer flow
    # (seed_views.py:735).
    Shot(seed_views.SeedExportXpubScriptTypeView, dict(seed_num=0, sig_type="ss"),
         filename="ScriptTypeOptions.png", run_before=use_address_explorer_flow,
         screen_kwargs=highlight("Native Segwit")),
    Shot(tools_views.ToolsAddressExplorerAddressTypeView,
         dict(seed_num=0, script_type=SettingsConstants.NATIVE_SEGWIT),
         filename="ReceiveAddressOptionSelectView.png",
         screen_kwargs=highlight("Receive Addresses")),
    Shot(tools_views.ToolsAddressExplorerAddressTypeView,
         dict(seed_num=0, script_type=SettingsConstants.NATIVE_SEGWIT),
         filename="ChangeAddressOptionSelectView.png",
         screen_kwargs=highlight("Change Addresses")),
    Shot(tools_views.ToolsAddressExplorerAddressTypeView,
         filename="AddressExplorerAddressTypeView.png",
         run_before=use_multisig_wallet,
         note="audit MS-3 -- must read 2/3, not 1/2"),
    Shot(tools_views.ToolsAddressExplorerAddressListView,
         filename="AddressExplorerReceiverAddressListView.png",
         run_before=use_address_explorer_seed),
    Shot(tools_views.ToolsAddressExplorerAddressListView, dict(is_change=True),
         filename="AddressExplorerChangeAddressListView.png",
         run_before=use_address_explorer_seed),

    # ===== Errors (audit C4) =====
    Shot(scan_views.ScanInvalidQRTypeView, filename="ScanInvalidQRTypeView.png",
         note="audit C4 -- the highest-value single orphan"),
    Shot(NotYetImplementedView, filename="NotYetImplementedView.png"),
    Shot(UnhandledExceptionView,
         dict(error=["IndexError", "line 1, in some_buggy_code.py",
                     "list index out of range"]),
         filename="UnhandledExceptionView.png"),
    Shot(NetworkMismatchErrorView, dict(derivation_path="m/84'/0'/0'"),
         filename="NetworkMismatchErrorView.png",
         note="audit -- network mismatch is the most-cited failure mode"),
    Shot(OptionDisabledView,
         dict(settings_attr=SettingsConstants.SETTING__MESSAGE_SIGNING),
         filename="OptionDisabledView.png"),

    # ===== Settings (audit C1-C3) =====
    Shot(settings_views.IOTestView, filename="IOTestView.png"),
    Shot(settings_views.DonateView, filename="DonateView.png"),

    # SettingsQR ingest confirmation -- audit D7 said no capture existed, but
    # upstream renders this View headlessly.
    Shot(settings_views.SettingsIngestSettingsQRView,
         dict(data=SETTINGS_QR_PERSISTENT),
         filename="SettingsIngestSettingsQRView_persistent.png", note="audit D7"),
    Shot(settings_views.SettingsIngestSettingsQRView,
         dict(data=SETTINGS_QR_EPHEMERAL),
         filename="SettingsIngestSettingsQRView_not_persistent.png", note="audit D7"),

    *_settings_menu_shots(),
    *_settings_value_picker_shots(),

    # A mainnet network picker, so contribute/testnet.md can show both states
    # (audit D9 -- no testnet-state capture existed anywhere).
    Shot(settings_views.SettingsEntryUpdateSelectionView,
         dict(attr_name=SettingsConstants.SETTING__NETWORK),
         filename="SettingsEntryUpdateSelectionView_network_mainnet.png",
         run_before=use_mainnet, note="audit D9"),
]

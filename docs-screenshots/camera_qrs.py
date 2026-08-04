"""Render the QR codes that belong inside the blank camera viewports (audit X-2).

The camera screens show one device photographing another device's screen. Nothing
headless can produce that frame, so the viewport is composited by hand — this
script supplies the QR that has to appear in it, built from the same fixture as
every other screenshot and encoded by SeedSigner's own encoders, so a reader who
decodes one gets the real value.

    python docs-screenshots/camera_qrs.py [--out DIR]

Writes one PNG per screen plus data.txt with the encoded payloads.
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import fixture  # noqa: E402  (sets up the SeedSigner app import path)

import qrcode  # noqa: E402
from embit import bip39  # noqa: E402
from embit.bip32 import HDKey  # noqa: E402
from embit.psbt import PSBT  # noqa: E402

from seedsigner.models.encode_qr import UrPsbtQrEncoder, UrXpubQrEncoder  # noqa: E402
from seedsigner.models.settings_definition import SettingsConstants  # noqa: E402

DENSITY = SettingsConstants.DENSITY__MEDIUM


def render(data: str, path: pathlib.Path, box_size: int = 12) -> None:
    """Plain black-on-white QR, sized for compositing down into a viewport."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    modules = qr.modules_count
    print(f"{path.name}: {modules}x{modules} modules, {len(data)} chars -> {img.size[0]}px")


def signed_psbt() -> PSBT:
    psbt = PSBT.from_string(fixture.PSBT_BASE64)
    root = HDKey.from_seed(
        bip39.mnemonic_to_seed(" ".join(fixture.MNEMONIC)),
        version=fixture.EMBIT_NETWORK["xprv"],
    )
    psbt.sign_with(root)
    return psbt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="docs-screenshots/out/camera-qrs")
    args = parser.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    payloads = {}

    # 1. AddressVerificationsCameraView — the device is looking at Sparrow's
    #    Receive tab, which shows a plain address QR.
    payloads["qr_receive_address"] = fixture.VERIFIED_ADDRESS

    # 2. SeedPSBTCameraView — the device is looking at Sparrow's animated
    #    "Show QR" of the unsigned transaction. Sparrow emits UR crypto-psbt,
    #    the same format this encoder produces.
    unsigned = UrPsbtQrEncoder(psbt=PSBT.from_string(fixture.PSBT_BASE64), qr_density=DENSITY)
    payloads["qr_psbt_unsigned_frame"] = unsigned.next_part()

    # 3. Sparrow_ScanKeystoreQR — Sparrow's webcam is looking at the device's
    #    xpub export. Sparrow's coordinator setting selects the UR encoder.
    xpub = UrXpubQrEncoder(
        seed=fixture.SEED,
        derivation=fixture.SINGLE_SIG_DERIVATION,
        network=fixture.NETWORK,
        qr_density=DENSITY,
        sig_type=SettingsConstants.SINGLE_SIG,
    )
    payloads["qr_xpub_sparrow"] = xpub.next_part()

    # 4. Sparrow_ScanSignedPSBT — Sparrow's webcam is looking at the device's
    #    signed PSBT, animated in the same UR format.
    signed = UrPsbtQrEncoder(psbt=signed_psbt(), qr_density=DENSITY)
    payloads["qr_psbt_signed_frame"] = signed.next_part()

    for name, data in payloads.items():
        render(data, out / f"{name}.png")

    lines = [f"fragments: unsigned {unsigned.seq_len()}, signed {signed.seq_len()}, "
             f"xpub {xpub.seq_len()}  (density: medium)", ""]
    for name, data in payloads.items():
        lines.append(f"--- {name} ---\n{data}\n")
    (out / "data.txt").write_text("\n".join(lines))
    print(f"\nwrote {out / 'data.txt'}")


if __name__ == "__main__":
    main()

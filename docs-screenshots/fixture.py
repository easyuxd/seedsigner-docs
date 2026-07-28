"""The canonical data every docs screenshot is rendered from.

One seed carries the whole single-sig journey (build-device -> first-wallet ->
receive -> send -> recover) so the fingerprint the reader is told to compare
actually matches on every screen. Three sibling seeds carry the 2-of-3 multisig
journey.

Entropy is derived from fixed tag strings, so the fixture is rebuildable from
this file alone -- no secret to lose, and the values in the prose can always be
re-derived and re-checked.

TESTNET ONLY. These mnemonics are published in a public docs repo and must never
hold value.
"""

import hashlib

import shim  # noqa: F401  -- must precede every seedsigner import

from embit import bip32, bip39, script
from embit.bip32 import HDKey
from embit.descriptor import Descriptor
from embit.networks import NETWORKS
from embit.psbt import PSBT, DerivationPath
from embit.transaction import Transaction, TransactionInput, TransactionOutput

from seedsigner.models.seed import Seed
from seedsigner.models.settings_definition import SettingsConstants

NETWORK = SettingsConstants.TESTNET
EMBIT_NETWORK = NETWORKS["test"]

SINGLE_SIG_DERIVATION = "m/84h/1h/0h"
MULTISIG_DERIVATION = "m/48h/1h/0h/2h"

_TAG = "seedsigner-docs canonical fixture v1"


def _mnemonic(tag: str) -> list[str]:
    """32 bytes of fixed entropy -> a valid 24-word mnemonic."""
    words = bip39.mnemonic_from_bytes(hashlib.sha256(tag.encode()).digest()).split()
    assert len(words) == 24
    return words


MNEMONIC = _mnemonic(_TAG)
MSIG_MNEMONICS = [_mnemonic(f"{_TAG} msig {i}") for i in (1, 2, 3)]

# The calc-final-word and dice flows are 12-word flows, and their final screen
# needs a mnemonic that actually checksums -- an invalid one makes the device
# report no fingerprint at all.
MNEMONIC_12 = bip39.mnemonic_from_bytes(
    hashlib.sha256(f"{_TAG} 12-word".encode()).digest()[:16]
).split()
assert len(MNEMONIC_12) == 12


def _seed(mnemonic: list[str]) -> Seed:
    return Seed(
        mnemonic=mnemonic,
        wordlist_language_code=SettingsConstants.WORDLIST_LANGUAGE__ENGLISH,
    )


SEED = _seed(MNEMONIC)
MSIG_SEEDS = [_seed(m) for m in MSIG_MNEMONICS]

FINGERPRINT = SEED.get_fingerprint(NETWORK)
MSIG_FINGERPRINTS = [s.get_fingerprint(NETWORK) for s in MSIG_SEEDS]


def _root(mnemonic: list[str]) -> HDKey:
    seed_bytes = bip39.mnemonic_to_seed(" ".join(mnemonic))
    return HDKey.from_seed(seed_bytes, version=EMBIT_NETWORK["xprv"])


def account_xpub(mnemonic: list[str], derivation: str) -> str:
    root = _root(mnemonic)
    return root.derive(derivation).to_public(version=EMBIT_NETWORK["xpub"]).to_string()


def receive_address(index: int = 0) -> str:
    key = _root(MNEMONIC).derive(f"{SINGLE_SIG_DERIVATION}/0/{index}")
    return script.p2wpkh(key).address(EMBIT_NETWORK)


XPUB = account_xpub(MNEMONIC, SINGLE_SIG_DERIVATION)

# The address the receive/verify screens show. Index 5 keeps continuity with the
# existing captures, whose "receive address index 5" the docs already reference.
VERIFIED_ADDRESS_INDEX = 5
VERIFIED_ADDRESS = receive_address(VERIFIED_ADDRESS_INDEX)


def multisig_descriptor() -> str:
    """2-of-3 native segwit, replacing upstream's 1-of-2 (audit finding MS-3)."""
    keys = []
    for mnemonic, fingerprint in zip(MSIG_MNEMONICS, MSIG_FINGERPRINTS):
        xpub = account_xpub(mnemonic, MULTISIG_DERIVATION)
        path = MULTISIG_DERIVATION.removeprefix("m/")
        keys.append(f"[{fingerprint}/{path}]{xpub}/{{0,1}}/*")
    return Descriptor.from_string(
        f"wsh(sortedmulti(2,{','.join(keys)}))"
    ).to_string()


MULTISIG_DESCRIPTOR = multisig_descriptor()


def address_verification_data() -> dict:
    """Payload for the address-verification screens."""
    return dict(
        address=VERIFIED_ADDRESS,
        network=NETWORK,
        sig_type=SettingsConstants.SINGLE_SIG,
        script_type=SettingsConstants.NATIVE_SEGWIT,
        derivation_path=SINGLE_SIG_DERIVATION.replace("h", "'"),
        verified_index=VERIFIED_ADDRESS_INDEX,
        verified_index_is_change=False,
    )


# ---------------------------------------------------------------------------
# The journey PSBT
#
# get-started/send.md is the audit's highest-severity gap (A1-A3, A7): the reader
# is told to scrutinise a review screen they have never been shown. Upstream's
# BASE64_PSBT_1 cannot fill it -- it is signable by `abandon x11`, not by the
# journey seed -- so the transaction has to be built from this fixture's wallet
# for PSBTParser to recognise the inputs as ours.
#
# Amounts are chosen to read clearly at 240x240 and to make the arithmetic on
# PSBTMathView verifiable by eye.
# ---------------------------------------------------------------------------

INPUT_AMOUNTS = [250_000, 100_000]   # sats, from receive addresses 0/0 and 0/1
SPEND_AMOUNT = 200_000
FEE_AMOUNT = 1_500
CHANGE_AMOUNT = sum(INPUT_AMOUNTS) - SPEND_AMOUNT - FEE_AMOUNT  # 148,500
CHANGE_INDEX = 0


def recipient_address() -> str:
    """An address outside the fixture wallet, so it renders as a real spend."""
    key = HDKey.from_seed(
        hashlib.sha256(f"{_TAG} recipient".encode()).digest(),
        version=EMBIT_NETWORK["xprv"],
    )
    return script.p2wpkh(key.derive("m/84h/1h/0h/0/0")).address(EMBIT_NETWORK)


RECIPIENT_ADDRESS = recipient_address()


def _fake_txid(tag: str) -> bytes:
    """A stable, plausible-looking previous-output txid."""
    return hashlib.sha256(f"{_TAG} utxo {tag}".encode()).digest()


def build_psbt() -> str:
    """An unsigned 2-input, 2-output testnet spend from the fixture wallet."""
    root = _root(MNEMONIC)
    fingerprint = root.my_fingerprint

    input_paths = [f"{SINGLE_SIG_DERIVATION}/0/{i}" for i in range(len(INPUT_AMOUNTS))]
    change_path = f"{SINGLE_SIG_DERIVATION}/1/{CHANGE_INDEX}"

    vin = [TransactionInput(_fake_txid(str(i)), 0) for i in range(len(INPUT_AMOUNTS))]
    vout = [
        TransactionOutput(SPEND_AMOUNT, script.address_to_scriptpubkey(RECIPIENT_ADDRESS)),
        TransactionOutput(CHANGE_AMOUNT, script.p2wpkh(root.derive(change_path))),
    ]
    psbt = PSBT(Transaction(version=2, vin=vin, vout=vout))

    # Inputs: the spent UTXO plus the derivation that proves it is ours.
    for i, (path, amount) in enumerate(zip(input_paths, INPUT_AMOUNTS)):
        key = root.derive(path)
        psbt.inputs[i].witness_utxo = TransactionOutput(amount, script.p2wpkh(key))
        psbt.inputs[i].bip32_derivations[key.to_public().key] = DerivationPath(
            fingerprint, bip32.parse_path(path)
        )

    # Only the change output carries a derivation; that is how the device tells
    # change from a payment.
    change_key = root.derive(change_path)
    psbt.outputs[1].bip32_derivations[change_key.to_public().key] = DerivationPath(
        fingerprint, bip32.parse_path(change_path)
    )

    return psbt.to_string()


PSBT_BASE64 = build_psbt()


# ---------------------------------------------------------------------------
# The multisig PSBT (audit D4)
#
# reference/multisig/spending.md walks a two-signature flow with no images. The
# witness scripts and key origins come from embit's Descriptor rather than being
# hand-assembled, so BIP-67 pubkey ordering inside `sortedmulti` stays correct.
# ---------------------------------------------------------------------------

MSIG_INPUT_AMOUNTS = [500_000]
MSIG_SPEND_AMOUNT = 300_000
MSIG_FEE_AMOUNT = 2_000
MSIG_CHANGE_AMOUNT = sum(MSIG_INPUT_AMOUNTS) - MSIG_SPEND_AMOUNT - MSIG_FEE_AMOUNT

_RECEIVE_BRANCH = 0
_CHANGE_BRANCH = 1


def _add_multisig_scope(scope, derived_descriptor):
    """Attach the witness script and every cosigner's derivation to one scope."""
    scope.witness_script = derived_descriptor.witness_script()
    for key in derived_descriptor.keys:
        scope.bip32_derivations[key.key.key] = DerivationPath(
            key.origin.fingerprint, key.origin.derivation
        )


def build_multisig_psbt() -> str:
    """An unsigned 2-of-3 testnet spend, awaiting its first signature."""
    descriptor = Descriptor.from_string(MULTISIG_DESCRIPTOR)

    inputs = [descriptor.derive(i, branch_index=_RECEIVE_BRANCH)
              for i in range(len(MSIG_INPUT_AMOUNTS))]
    change = descriptor.derive(CHANGE_INDEX, branch_index=_CHANGE_BRANCH)

    vin = [TransactionInput(_fake_txid(f"msig {i}"), 0) for i in range(len(inputs))]
    vout = [
        TransactionOutput(MSIG_SPEND_AMOUNT,
                          script.address_to_scriptpubkey(RECIPIENT_ADDRESS)),
        TransactionOutput(MSIG_CHANGE_AMOUNT, change.script_pubkey()),
    ]
    psbt = PSBT(Transaction(version=2, vin=vin, vout=vout))

    # Global xpubs: how the device recognises the cosigners as a known quorum.
    for key in descriptor.keys:
        psbt.xpubs[key.key] = DerivationPath(
            key.origin.fingerprint, key.origin.derivation
        )

    for i, (derived, amount) in enumerate(zip(inputs, MSIG_INPUT_AMOUNTS)):
        psbt.inputs[i].witness_utxo = TransactionOutput(amount, derived.script_pubkey())
        _add_multisig_scope(psbt.inputs[i], derived)

    _add_multisig_scope(psbt.outputs[1], change)

    return psbt.to_string()


MULTISIG_PSBT_BASE64 = build_multisig_psbt()


def summary() -> str:
    """Printed by generate.py so the prose can be reconciled against reality."""
    lines = [
        "Canonical docs fixture (testnet)",
        f"  mnemonic       {' '.join(MNEMONIC[:6])} ... {MNEMONIC[-1]}",
        f"  fingerprint    {FINGERPRINT}",
        f"  derivation     {SINGLE_SIG_DERIVATION.replace('h', chr(39))}",
        f"  account xpub   {XPUB[:20]}...{XPUB[-6:]}",
        f"  address [0/{VERIFIED_ADDRESS_INDEX}]  {VERIFIED_ADDRESS}",
        f"  msig 2-of-3    {' / '.join(MSIG_FINGERPRINTS)}",
        f"  psbt           {sum(INPUT_AMOUNTS):,} in -> {SPEND_AMOUNT:,} spend "
        f"+ {CHANGE_AMOUNT:,} change + {FEE_AMOUNT:,} fee",
        f"  recipient      {RECIPIENT_ADDRESS}",
    ]
    return "\n".join(lines)

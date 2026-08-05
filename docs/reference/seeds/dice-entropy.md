# Dice entropy explained

> The math behind 50 and 99 dice rolls — why those numbers, how rolls become words, and how to verify the result independently.

Dice-based seed generation ([how-to here](/reference/seeds/creation.md#method-2-dice-based-seed-generation)) uses physical dice for randomness rather than code or hardware. This page explains *why* it works.

## How much randomness is in a dice roll?

A fair six-sided die has 6 equally likely outcomes, so each roll contributes **log₂(6) ≈ 2.585 bits** of entropy. Security targets for BIP-39 seeds are defined in bits:

| Seed length | Entropy required | Rolls needed | Rolls SeedSigner asks for |
|-------------|------------------|--------------|---------------------------|
| 12 words | 128 bits | 128 ÷ 2.585 ≈ 49.5 → 50 | **50** |
| 24 words | 256 bits | 256 ÷ 2.585 ≈ 99.0 → 99 | **99** |

Fifty rolls give 6⁵⁰ ≈ 2¹²⁹ possible sequences — comfortably past the 128-bit target. Ninety-nine rolls give 6⁹⁹ ≈ 2²⁵⁵·⁹, effectively the full 256-bit strength (and the same roll count used by other hardware wallets' dice modes).

To put 128 bits in perspective: guessing a 12-word seed by brute force means searching 2¹²⁸ ≈ 3.4 × 10³⁸ possibilities. That is beyond any realistic computation — which is why the *quality* of your rolls matters more than adding more of them.

## From rolls to words

1. You enter each roll (1–6) on the device; SeedSigner records the sequence.
2. The full roll sequence is hashed with **SHA-256**, producing a uniformly distributed string of bits. Hashing means the entropy is spread evenly even though raw dice digits aren't a power of two.
3. The first 128 (or 256) bits become the seed's entropy. A **checksum** (the first bits of a second SHA-256 hash) is appended: 4 bits for 12 words, 8 bits for 24.
4. The combined bits are split into 11-bit groups, and each group indexes one of the 2,048 words in the BIP-39 word list. That's why 24 × 11 = 264 = 256 entropy + 8 checksum.

The process is fully deterministic: **the same rolls always produce the same seed phrase**, which is what makes independent verification possible.

## Verifying independently

Because the derivation is deterministic and standard, you can check that SeedSigner isn't cheating (or buggy):

1. Write down your roll sequence as you enter it.
2. On a **separate, permanently offline** computer, run an independent implementation — for example the SeedSigner project's own [dice verification procedure](https://github.com/SeedSigner/seedsigner/blob/main/docs/dice_verification.md), or an offline copy of a BIP-39 tool that accepts dice entropy.
3. Confirm the independently computed phrase matches SeedSigner's output word for word.

> **Warning:** Never type real roll sequences or seed words into an internet-connected computer. Do verification offline, then treat the test rolls as burned — generate a fresh seed for actual use if there's any doubt.

## Dice quality and technique

The math above assumes **fair** dice. In practice:

- **Use a casino-grade die** if you can — they're precision-balanced. Ordinary dice are slightly biased but fine in combination with the roll counts above; heavily worn or novelty dice are worse.
- **Roll properly**: shake and throw onto a hard, flat surface. Don't "place" or half-heartedly tip the die.
- **Enter every roll as it lands.** Don't skip results that "feel" non-random (real randomness produces runs and repeats), and never reorder or cherry-pick — human filtering *removes* entropy.
- Rolling a few extra times at the start to warm up is harmless; editing the sequence afterward is not.

> **Tip:** Bias hurts less than you'd think — the SHA-256 step mixes the sequence thoroughly, and 50/99 rolls carry margin above the strict minimum. The real risks are lazy rolling technique and doing the rolls where a camera (including your own phone) can see them.

## Related pages

- [Seed creation](/reference/seeds/creation.md): the step-by-step dice procedure on the device.
- [Seed verification](/reference/seeds/verification.md): backup-check your new seed.
- [Security model](/security/overview.md): where trust-minimized entropy fits in the bigger picture.

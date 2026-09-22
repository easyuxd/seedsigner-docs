# Dice entropy explained

> Roll a seed privately and independently, then let SeedSigner convert the results into a BIP-39 seed phrase.

> **Warning:** The dice-quality measurements and implementation-history claims on this page come from [AI-assisted analyses](https://kdmukai-bot.github.io/seedsigner-ai-analysis/dice/standard.html) directed by SeedSigner's lead developer. They are not an independent audit, a certification, or an official SeedSigner project publication. The available dice measurements are limited and do not cover every die or rolling technique. The current conversion method was cross-checked against SeedSigner 0.8.7 source code, its published test vectors, and BIP-39. Treat the guidance as evidence, not a security guarantee.

Dice let you create the only unpredictable input yourself. SeedSigner then performs a deterministic conversion: the same entered rolls always produce the same words. This makes the method testable, but it also makes your rolling procedure and privacy part of the security boundary. For the on-device steps, follow [dice-based seed generation](/reference/seeds/creation.md#method-2-dice-based-seed-generation).

## Before you roll

1. **Use an ordinary, undamaged six-sided die.** Casino-grade dice are more precisely made, but the available measurements do not show a practical reason to buy one for this process. Replace any die that is visibly damaged, badly misshapen, known to be loaded, or unable to tumble freely.
2. **Prepare a private workspace.** Keep the die, SeedSigner screen, and results away from other people, cameras, and windows. Do not read the results aloud near a microphone or voice assistant.
3. **Use a hard, contained rolling area.** A tray, dice cup, or roomy lidded box helps the die tumble, bounce, and stay out of view.
4. **Test the process before creating a real seed.** Complete at least one full, genuinely rolled test set and compare its words with an independent implementation of SeedSigner's method. Treat that seed as disposable and never fund it.

> **Warning:** Never enter the rolls or words for a real seed into a second tool or device, even if it is offline. Every copy creates another place the seed can leak from. Use disposable test rolls to verify the process before you generate the seed you intend to keep.

## How to roll

1. **Give every roll a thorough tumble.** Shake or throw the die so it turns repeatedly and bounces several times before settling. Dropping or gently tipping a die can preserve its starting orientation and make successive results less independent.
2. **Enter every result exactly once.** Record rolls in the order they land. Do not skip, reroll, rearrange, or replace a result because it looks unusual.
3. **Expect streaks and repeats.** Random sequences often contain both. Editing them to look more balanced makes the sequence more predictable.
4. **Complete the count SeedSigner requires.** Enter 50 rolls for a 12-word seed or 99 rolls for a 24-word seed. SeedSigner does not finish early or accept extra rolls in this flow.

One die is the simplest arrangement. To save time, you can shake several distinguishable dice in a roomy lidded box. Choose a fixed reading order, such as by color, before the first shake. Never sort the dice by the values rolled.

> **Note:** A short set of 50 or 99 results cannot reliably prove that a die is fair. Use a die without an obvious defect and focus on thorough tumbling, private rolls, and accurate entry.

## Verify with disposable test rolls

Verification checks that SeedSigner converts the digits as documented. It does not require exposing the rolls that protect real funds.

1. **Roll a complete test set.** Use 50 or 99 physical rolls and enter them exactly as you would for a real seed.
2. **Write down the test results.** Mark the roll sequence and resulting words as disposable so they cannot be mistaken for a real backup.
3. **Run an independent check.** Follow SeedSigner's [published dice verification procedure](https://github.com/SeedSigner/seedsigner/blob/0.8.7/docs/dice_verification.md), or use another implementation that explicitly reproduces SeedSigner's conversion.
4. **Compare every word.** The independent result must match SeedSigner word for word. Resolve any mismatch before creating a real seed.
5. **Discard the test seed.** Never receive bitcoin to it. Repeat with a fresh test set if you want additional assurance.

Different wallets and tools use incompatible dice conversions. SeedSigner hashes the characters `1` through `6` exactly as entered. Other methods may rewrite `6` as `0`, pack the rolls into bits, or interpret them as a base-6 number. A tool using one of those methods produces different words without either tool being defective.

For a real seed, enter each result directly into SeedSigner and do not retain a roll transcript. If you do write the rolls down, protect them like the seed phrase: anyone with the complete sequence can recreate the same words.

## Why SeedSigner asks for 50 or 99 rolls

A fair six-sided die has six equally likely results. One independent roll therefore carries **log₂(6) ≈ 2.585 bits** of uncertainty.

| Seed length | Rolls SeedSigner accepts | Uncertainty in fair roll sequence | BIP-39 entropy field |
|-------------|--------------------------|-----------------------------------|----------------------|
| 12 words | **50** | 50 × log₂(6) ≈ **129.25 bits** | 128 bits |
| 24 words | **99** | 99 × log₂(6) ≈ **255.91 bits** | 256 bits |

For 12 words, the roll sequence contains slightly more uncertainty than the 128-bit field can hold. SeedSigner keeps the first 128 bits of the SHA-256 result. For 24 words, 99 fair rolls fall about 0.09 bit below the field's 256-bit capacity. That difference is not practically meaningful, but it is more accurate than calling 99 rolls a full 256 bits.

Extra rolls are not part of SeedSigner's method. Its fixed counts produce the intended 12- or 24-word result, and the device accepts no additional entries in this flow.

## From rolls to words

SeedSigner 0.8.7 performs these steps:

1. It joins the entered results into one string of text containing only the characters `1` through `6`.
2. It hashes that string once with **SHA-256**, producing 256 output bits.
3. For a 12-word seed, it keeps the first 128 bits. For a 24-word seed, it uses all 256 output bits.
4. It appends the BIP-39 checksum: 4 bits for 12 words or 8 bits for 24 words.
5. It splits the result into 11-bit groups. Each group selects one of the 2,048 words in the BIP-39 word list.

Hashing spreads the unpredictability already present in the rolls across the output. It does **not** create entropy that was lost through predictable choices, weak tumbling, correlated rolls, or an exposed sequence.

## What not to worry about

- **Ordinary dice:** Available studies found small biases in inexpensive dice, although the evidence is limited. A visibly sound die with a thorough tumble is appropriate for this method.
- **Runs and repeated faces:** These are expected in genuinely random data. Do not edit them.
- **Buying casino dice:** Precision dice are fairer, but the measured difference is not a reason to replace an ordinary undamaged die for this use.
- **Testing a die from 50 or 99 rolls:** That sample is too small to distinguish ordinary manufacturing bias from normal variation.
- **Adding extra rolls:** SeedSigner deliberately accepts a fixed count. More rolls are not part of this conversion.

## Where these claims come from

The practical dice guidance and dice-quality discussion come from **[Dice to seed](https://kdmukai-bot.github.io/seedsigner-ai-analysis/dice/standard.html)**. It is a living, AI-assisted analysis covering five dice-conversion methods across 17 implementations. Its dice-quality evidence relies mainly on two published experiments from 1971 and 2009, and the analysis documents the limits of both.

The SeedSigner-specific implementation and history claims come from **[SeedSigner dice entropy](https://kdmukai-bot.github.io/seedsigner-ai-analysis/dice/)**, an AI-assisted analysis of release 0.8.7 and earlier releases. Its author provides scripts and commands intended to reproduce the results, but explicitly states that the work is not an audit or certification.

The current conversion can also be checked against SeedSigner's [0.8.7 source code](https://github.com/SeedSigner/seedsigner/blob/0.8.7/src/seedsigner/helpers/mnemonic_generation.py) and [published verification vectors](https://github.com/SeedSigner/seedsigner/blob/0.8.7/docs/dice_verification.md). The checksum and word encoding follow the [BIP-39 specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki). See the warning at the top of this page for the limits that still apply.

## Related pages

- [Seed creation](/reference/seeds/creation.md): the step-by-step dice procedure on the device.
- [Image entropy explained](/reference/seeds/image-entropy.md): the alternative method, with a different verification trade-off.
- [Seed verification](/reference/seeds/verification.md): backup-check your new seed.
- [Security model](/security/overview.md): where trust-minimized entropy fits in the bigger picture.

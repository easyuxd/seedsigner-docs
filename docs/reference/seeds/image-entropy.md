# Image entropy explained

> Take a photo, get a seed phrase. [Camera-based seed generation](/reference/seeds/creation.md#method-1-camera-based-seed-generation) turns a single photograph into a BIP-39 seed phrase.

> **Warning:** Every measurement on this page comes from a single source: an [AI-assisted analysis](https://kdmukai-bot.github.io/seedsigner-ai-analysis/image-entropy/) published by SeedSigner's lead developer. By its own statement it is not an independent audit, not a certification, and not an official SeedSigner project publication, and no third party has yet reproduced its figures. The raw camera data is published so that anyone can check the work, but until someone does, treat these numbers as the best available evidence rather than settled fact. Nothing here is a security guarantee.

## What goes into the seed

SeedSigner builds the seed as a running SHA-256 chain, folding in four inputs in order:

| # | Input | What it contributes |
|---|-------|---------------------|
| 1 | **CPU serial number** | A fixed, non-secret per-device value. Makes two devices differ; adds no real unpredictability. |
| 2 | **System time** | SeedSigner has no real-time clock and no network, so the clock starts at zero every boot. This is just fractional seconds since power-on: bounded, and not something to lean on. |
| 3 | **Live preview frames** | A rolling window of up to **50 frames at 240 × 240**, captured while you aim the camera. |
| 4 | **The final photograph** | One full-resolution capture at **480 × 480**. |

Each step hashes the previous digest together with the new data, so the final digest depends on all four. The resulting 256-bit digest becomes the seed: all 256 bits for a 24-word phrase, or the first 128 bits for a 12-word phrase. From there it's the same path as dice. A checksum is appended, the bits are split into 11-bit groups, and each group indexes one of the 2,048 BIP-39 words.

> **Note:** SHA-256 always emits 256 bits, however much data goes in. Once 256 bits of genuine unpredictability have gone into the chain, everything beyond that is extraneous. It still changes the result, but it can't make the seed harder to attack. So 256 bits is a **threshold**, not a score to beat, and a big margin just means the threshold was cleared with room to spare.

## The randomness is in the sensor, not the scene

A 240 × 240 preview frame holds about 1.38 million bits; the final image holds about 5.53 million. Fifty preview frames plus the final image is roughly 74.6 million bits entering the chain, against the 256 a 24-word seed needs. But raw capacity isn't entropy. A frame is only a container, and what it carries depends on what the sensor actually collected.

What fills it is **sensor noise**: heat in the sensor, plus imprecision in the readout electronics that turn collected light into numbers. Every exposure carries a fresh dose of it, so no two captures are ever byte-identical. And because a hash has no notion of similarity, a nearly identical photograph produces a completely unrelated seed.

## Capture technique

> **Warning:** Never capture with the lens covered, face-down, or pointed into a bag or an unlit space. No error appears, and the resulting seed may rest on a far thinner margin than the method is designed to provide. If you think you may have done this, generate a fresh seed.

- **Point at any lit scene.** Trees, a bookshelf, a blank wall, a room. It genuinely doesn't matter what you photograph, only that it's lit. Every lit capture on every device tested cleared the requirement thousands of times over.
- **Don't aim into a bright light source.** A saturated sensor reads maximum everywhere and the frame-to-frame variation is truncated. This takes deliberate effort to arrange; ordinary well-lit rooms and windows are fine.
- **Tap the button, don't hold it.** Holding a button down carries you through the preview, capture and accept screens in one gesture, and the code returns before any preview frame is chained. That silently drops input 3 entirely, in any lighting.
- **Give the preview a few seconds.** The 50-frame window fills in roughly three and a half to six seconds of live preview, so the time you spend aiming is already doing that work. Holding the preview open longer doesn't add more frames, only fresher ones.
- **Watch the preview, and know what it proves.** A moving live image confirms the camera is alive and seeing light. That check is real and worth doing, but the screen only tells you the camera works. The scene decides what it collects.

## What you can verify, and what you can't

Camera entropy sits in a different trust relationship from dice, and the difference is structural rather than a matter of code quality.

SeedSigner never writes a secret to persistent storage. The preview frames and the final photograph exist only in RAM, are fed through the SHA-256 chain, and are released. Nothing is saved to the microSD card. Exporting them isn't practical either: the inputs total roughly 12 MB, and SeedSigner's only outbound channel is the screen, where a QR code carries a few kilobytes.

The consequence: **you can verify the process, but not the individual outcome.** Nobody can go back afterwards and confirm anything about a specific camera-generated seed. What you *can* do:

1. **Verify the process.** The code is open, and the chain above is exactly what it does with the bytes.
2. **Verify you're running that code.** Release images have been reproducible since v0.7.0, so the strong form is to build from source and confirm you get the published image byte for byte. The weaker form is to [check the published hash and PGP signature](/reference/software/verify-image.md).
3. **Choose the scene.** The only per-capture control, and the only step nobody else can perform for you.

> **Tip:** None of this makes camera entropy weaker than dice. A lit capture feeds the chain orders of magnitude more unpredictability than a dice session does. The trade-off is verifiability: dice rolls are small enough to write on paper, so an individual dice result stays externally checkable forever. If after-the-fact verification matters to you, use [dice entropy](/reference/seeds/dice-entropy.md) instead.

## Where these figures come from

Every measurement quoted above is drawn from **[SeedSigner image entropy](https://kdmukai-bot.github.io/seedsigner-ai-analysis/image-entropy/)**, an AI-assisted analysis covering release 0.8.7 across 32 capture runs on 4 devices. Roughly 340 MB of raw camera frames are published alongside it, together with the methods and the commands needed to recompute every number. Its author explicitly welcomes corrections and challenges to the measurements. See the warning at the top of this page for the caveats that come with it.

## Related pages

- [Seed creation](/reference/seeds/creation.md): the step-by-step camera procedure on the device.
- [Dice entropy explained](/reference/seeds/dice-entropy.md): the alternative method, and the one whose result you can check independently.
- [Seed verification](/reference/seeds/verification.md): backup-check your new seed.
- [Security model](/security/overview.md): where trust-minimized entropy fits in the bigger picture.

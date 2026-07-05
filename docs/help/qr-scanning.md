# QR scanning troubleshooting

> Fix slow, stalled, or failed QR scans — in both directions: SeedSigner reading your coordinator's screen, and your coordinator reading SeedSigner's screen.

QR codes are SeedSigner's **only** communication channel, so when scanning misbehaves the whole workflow stops. The good news: nearly every scanning problem comes down to one of four factors: **lighting, distance, focus, or QR density**. All four are fixable in minutes.

This page is organized by direction. First figure out which side is struggling:

| Symptom | Struggling side | Jump to |
|---------|-----------------|---------|
| SeedSigner's progress bar stalls or crawls while scanning an animated QR | SeedSigner's camera | [Scanning *into* SeedSigner](#scanning-into-seedsigner) |
| SeedSigner never recognizes a code at all | SeedSigner's camera | [Scanning *into* SeedSigner](#scanning-into-seedsigner) |
| Sparrow / your phone won't pick up the QR on SeedSigner's screen | Coordinator's camera | [Scanning *from* SeedSigner's screen](#scanning-from-seedsigners-screen) |

---

## How SeedSigner scanning works

Large payloads (PSBTs, xpubs, descriptors) don't fit in a single QR code, so they are split across an **animated** sequence of frames. SeedSigner must capture *every* frame — the progress bar shows how many it still needs. Missed frames simply come around again on the next loop, which is why a struggling scan gets *slow* rather than failing outright.

Two practical consequences:

- **You don't have to catch frames in order.** Hold steady and let the loop repeat.
- **Fewer, simpler frames scan faster.** That's what the density settings below control.

## Scanning *into* SeedSigner

Work through these in order — the first three resolve most cases.

### 1. Fix the lighting

The camera needs even, adequate light on the code — but **not** glare.

- Scanning a **paper** QR (SeedQR backup): use bright, indirect light. Avoid harsh shadows across the code.
- Scanning a **screen** (Sparrow, phone): try **lowering the room lights** to reduce reflections on the monitor, and make sure no window or lamp reflects off the screen at the camera's angle.

### 2. Adjust the distance

Hold SeedSigner **6 to 12 inches (15–30 cm)** from the code. Too close and the fixed-focus lens can't resolve it; too far and the modules are too small. Move slowly closer and further until the scan picks up speed — there's a sweet spot.

### 3. Clean (and check) the lens

A fingerprint or dust speck on the tiny lens dramatically degrades scanning. Wipe it gently with a microfiber cloth.

> **Tip:** Many OV5647 camera modules ship with a **protective film over the lens:** if your camera has never scanned well, check that the film was removed. Some modules also have an adjustable focus ring; if yours does and close-range scanning has always been poor, a very slight rotation can bring the 6–12 inch range into focus.

### 4. Lower the density on the *sending* side

If SeedSigner is scanning an animated QR from your coordinator, make each frame easier to read:

- **Sparrow:** the QR display window has controls to reduce the **density** (module count per frame) and slow the **frame rate**. Larger, slower frames are much easier for the camera to capture. Increase the QR's on-screen size too.
- **Phone wallets:** turn the phone's screen brightness up and hold it as flat and steady as possible.

### 5. Check SeedSigner's camera settings

- If the camera preview is rotated or upside-down, fix **Settings > Advanced > Camera Rotation** (cycle 0° / 90° / 180° / 270° until the preview is right-side up). A rotated image can still scan, but a correctly oriented preview makes aiming much easier.
- While the scanning screen is open, push the joystick **up or down** to adjust the preview exposure/brightness — this often unsticks a stalled scan of a bright monitor.

### 6. Confirm the camera works at all

Run **Settings > I/O Test**. If the camera shows no image:

1. Power off and re-seat the **camera ribbon cable** at both ends — the contacts must face the correct side and the latch must be fully closed.
2. Confirm you used the **Zero-compatible ribbon cable** (narrower, gold connector) if your board is a Pi Zero.
3. Try a different cable or camera module if available — ribbon cables are fragile and fail from repeated flexing.

## Scanning *from* SeedSigner's screen

When your coordinator's webcam or phone camera struggles to read SeedSigner's 240×240 display:

### 1. Lower SeedSigner's QR density

Go to **Settings > Advanced > QR Density** and select **Low**. Each frame becomes larger and simpler — the single most effective fix for a coordinator that can't keep up. The transfer takes more frames, but each one actually scans.

### 2. Adjust SeedSigner's screen brightness

While SeedSigner is displaying a QR code, push the joystick **up or down** to change the screen brightness. A too-bright screen blooms and washes out the QR modules on camera; a dim screen disappears in a bright room. Adjust until the code looks crisp in your coordinator's camera preview.

### 3. Help the webcam focus

- Hold the device **8–12 inches** from the webcam and keep it as still as you can (brace your elbows on the desk).
- Cheap webcams have poor close-range focus. If yours never locks on, try moving *further* away, or use a phone camera instead — most phone cameras outperform built-in laptop webcams at this.
- Clean the webcam lens and avoid backlighting (don't sit with a bright window behind the device).

### 4. Give the coordinator a bigger target

In Sparrow, enlarge the camera preview window and choose a higher webcam resolution in **Preferences** if scanning is unreliable.

## Quick reference: the density trade-off

| QR Density (Settings > Advanced) | Frame size | Frames needed | Best when |
|----------------------------------|-----------|---------------|-----------|
| **Low** | Large, simple | Most | Webcam or lighting is marginal — prioritize reliability |
| **Medium** (default) | Balanced | Moderate | Most setups |
| **High** | Small, dense | Fewest | Good camera, good light — prioritize speed |

## Still stuck?

- Work through the [device-side checks in Common issues](/help/common-issues.md) — power and connection problems can masquerade as camera problems.
- Confirm the exact failure with **Settings > I/O Test** (camera, buttons, and display all in one screen).
- Ask the community — see [Resources & links](/help/resources.md).

> **Tip:** When testing fixes, use a low-stakes payload — export an xpub or scan a test SeedQR rather than repeatedly rebuilding a real transaction.

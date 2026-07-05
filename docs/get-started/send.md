# Send bitcoin

> Build a transaction in your coordinator, **review and sign it on SeedSigner's trusted screen**, then broadcast it — bouncing the transaction back and forth as QR codes.

Spending is the half that requires your keys, so SeedSigner does the signing. Your coordinator builds an unsigned transaction (a **PSBT** — Partially Signed Bitcoin Transaction), SeedSigner shows you exactly what you're authorizing and signs it, and the coordinator broadcasts the result.

## What you need

- A SeedSigner with the correct seed loaded ([load it](/reference/seeds/loading.md) if needed).
- A funded watch-only wallet in your coordinator (Sparrow, etc.).
- A webcam on your computer for scanning QR codes.

## The journey at a glance

<figure class="ss-diagram ss-swimlane" aria-label="The four steps of sending bitcoin: build the transaction in the coordinator, scan it into SeedSigner, review every detail on the device screen, then sign and broadcast">
  <div class="ss-lane-heads">
    <span class="ss-lane-head ss-lane-head--computer">Coordinator <em>Sparrow &middot; networked</em></span>
    <span class="ss-gap-label" aria-hidden="true">&#8646; QR only</span>
    <span class="ss-lane-head ss-lane-head--device">SeedSigner <em>air-gapped</em></span>
  </div>
  <ol class="ss-steps">
    <li class="ss-step ss-step--computer"><span class="ss-step-num">1</span><span class="ss-lane-tag ss-lane-tag--computer">Coordinator</span><span class="ss-step-body">Build the transaction<small>Show it as an animated PSBT QR</small></span><span class="ss-qr-badge"><span class="ss-sr">unsigned transaction sent to SeedSigner by </span>QR<span aria-hidden="true">&nbsp;&#9658;</span></span></li>
    <li class="ss-step ss-step--device"><span class="ss-step-num">2</span><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span><span class="ss-step-body">Scan the PSBT</span></li>
    <li class="ss-step ss-step--device ss-step--warn"><span class="ss-step-num">3</span><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span><span class="ss-step-body">Review recipient / amount / fee / change<small>The whole reason to use a signer &mdash; check all four</small></span></li>
    <li class="ss-step ss-step--handoff"><span class="ss-step-num">4</span><span class="ss-handoff-half ss-handoff-half--computer">Scan the signed QR back in &#8594; Broadcast</span><span class="ss-qr-badge"><span class="ss-sr">signature returned to the coordinator by </span>QR<span aria-hidden="true">&nbsp;&#9668;</span></span><span class="ss-handoff-half ss-handoff-half--device">Approve &#8594; the signed QR appears</span></li>
  </ol>
  <figcaption class="ss-caption">The PSBT goes in as one QR and the signature comes back as another &mdash; your keys never leave the device, and step 3 happens on a screen malware can't touch.</figcaption>
</figure>

---

## Step 1: Build the transaction in your coordinator

In your coordinator, create the send: enter the recipient address and amount, choose a fee, and generate the transaction. Display it as an **animated PSBT QR code** (in Sparrow, **Show QR** on the transaction).

## Step 2: Scan the PSBT into SeedSigner

On SeedSigner, from the loaded seed's menu select **Scan PSBT** (or **Scan** from the main menu), then point the camera at the animated QR on your computer. The device reads multiple frames and reassembles the full transaction. Full detail: [PSBT signing](/reference/keys/psbt-signing.md).

## Step 3: Review every detail — this is the important part

SeedSigner shows you the transaction on a screen that malware on your computer **cannot** tamper with. Check all four:

| Check | What to look for |
|-------|------------------|
| **Recipient address** | Matches your intended destination, character for character |
| **Amount** | The correct amount of bitcoin to send |
| **Network fee** | Reasonable for current conditions |
| **Change address** | Change returns to **your own** wallet |

> **Warning:** Bitcoin transactions are irreversible once broadcast. Always verify the recipient address on SeedSigner's screen — a compromised computer could swap the address your coordinator showed. This on-device review is the whole reason to use a signer.

## Step 4: Approve and hand the signature back

1. If multiple seeds are loaded, select the correct signing seed.
2. Select **Approve PSBT**. SeedSigner adds the signature and displays a new animated QR.
3. In your coordinator, choose **Scan QR** and point your webcam at SeedSigner's screen to read the signed transaction back in.
4. Click **Broadcast Transaction** to send it to the Bitcoin network.

> For a multi-sig wallet, repeat the scan-review-sign cycle with each required cosigner until the quorum is met — see [Set up multisig](/get-started/multisig.md) and [Multisig spending](/reference/multisig/spending.md).

---

## You're done — checklist

- [ ] Transaction built and shown as a PSBT QR in the coordinator.
- [ ] Recipient, amount, fee, and change **reviewed on SeedSigner**.
- [ ] PSBT approved and signed; signed QR scanned back into the coordinator.
- [ ] Transaction broadcast and confirming.

## Where to go next

- [PSBT signing](/reference/keys/psbt-signing.md) — the full screen-by-screen reference, including scanning tips.
- [Receive bitcoin](/get-started/receive.md) — the other half of using your wallet.
- [Set up multisig](/get-started/multisig.md) — require multiple keys to spend.

> **Tip:** Trouble getting the QR to scan in either direction? Lower **QR Density** in SeedSigner settings for larger codes, and improve lighting. More: [QR scanning troubleshooting](/help/qr-scanning.md).

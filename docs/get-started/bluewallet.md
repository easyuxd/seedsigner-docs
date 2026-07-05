# Use a mobile coordinator (BlueWallet)

> Run your watch-only wallet on your **phone** instead of a desktop — import your xpub into BlueWallet, then receive and sign on the go with QR codes.

Everything in the other journeys assumes Sparrow on a computer, but a coordinator can just as well be a phone. BlueWallet (iOS / Android) speaks the same language: it imports your public key, watches the chain, builds PSBTs, and trades QR codes with SeedSigner. Your keys still never touch a networked device — the phone only ever sees public data and signed transactions.

## What you need

- A SeedSigner with your seed loaded ([create](/get-started/first-wallet.md) or [load](/reference/seeds/loading.md) one first).
- [BlueWallet](https://bluewallet.io) installed on your phone.

> **Warning:** BlueWallet does **not support testnet**, so you can't practice this journey with test coins. If you're new, do the [first wallet journey](/get-started/first-wallet.md) with Sparrow on testnet first, then set up BlueWallet — and start with a small amount.

## The journey at a glance

<figure class="ss-diagram ss-swimlane" aria-label="The five steps of using BlueWallet as a mobile coordinator: export the xpub from SeedSigner into BlueWallet as a watch-only wallet, verify a receive address on the device, then build, sign, and broadcast a transaction with two QR handoffs">
  <div class="ss-lane-heads">
    <span class="ss-lane-head ss-lane-head--computer">Coordinator <em>BlueWallet &middot; phone</em></span>
    <span class="ss-gap-label" aria-hidden="true">&#8646; QR only</span>
    <span class="ss-lane-head ss-lane-head--device">SeedSigner <em>air-gapped</em></span>
  </div>
  <ol class="ss-steps">
    <li class="ss-step ss-step--device"><span class="ss-step-num">1</span><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span><span class="ss-step-body">Export your xpub<small>Public key only &mdash; nothing secret</small></span><span class="ss-qr-badge"><span class="ss-sr">xpub sent to the phone by </span>QR<span aria-hidden="true">&nbsp;&#9668;</span></span></li>
    <li class="ss-step ss-step--computer"><span class="ss-step-num">2</span><span class="ss-lane-tag ss-lane-tag--computer">BlueWallet</span><span class="ss-step-body">Import it as a watch-only wallet</span></li>
    <li class="ss-step ss-step--device ss-step--warn"><span class="ss-step-num">3</span><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span><span class="ss-step-body">Verify a receive address on the device<small>Confirms the phone imported <strong>your</strong> keys</small></span></li>
    <li class="ss-step ss-step--computer"><span class="ss-step-num">4</span><span class="ss-lane-tag ss-lane-tag--computer">BlueWallet</span><span class="ss-step-body">Build a transaction<small>Shown as an animated PSBT QR</small></span><span class="ss-qr-badge"><span class="ss-sr">unsigned transaction sent to SeedSigner by </span>QR<span aria-hidden="true">&nbsp;&#9658;</span></span></li>
    <li class="ss-step ss-step--handoff"><span class="ss-step-num">5</span><span class="ss-handoff-half ss-handoff-half--computer">Scan the signed QR &#8594; Broadcast</span><span class="ss-qr-badge"><span class="ss-sr">signature returned to the phone by </span>QR<span aria-hidden="true">&nbsp;&#9668;</span></span><span class="ss-handoff-half ss-handoff-half--device">Review on device &#8594; sign</span></li>
  </ol>
  <figcaption class="ss-caption">Same air-gapped pattern as the desktop journeys &mdash; only the coordinator moved into your pocket.</figcaption>
</figure>

---

## Step 1: Export your xpub from SeedSigner

1. Make sure **BlueWallet** is enabled under **Settings > Coordinator Software** so the export uses the format BlueWallet expects.
2. From the main menu select **Seeds**, choose your seed, then **Export Xpub**.
3. Choose **Single Sig**, keep the default **Native Segwit** script type, and select **BlueWallet** as the coordinator.
4. Review the xpub details, then SeedSigner displays the export as a QR code.

This is your **extended public key** — it lets a wallet watch balances and generate addresses, but it cannot spend. Full detail: [Xpub export](/reference/keys/xpub-export.md).

## Step 2: Import it into BlueWallet

1. In BlueWallet, tap **Add Wallet**, then choose **Import wallet**.
2. Choose to **scan a QR code** and point the phone's camera at SeedSigner's screen.
3. BlueWallet creates a **watch-only** wallet from the key. Give it a recognizable name.

The wallet shows a balance of zero and can generate receive addresses — but it will always need SeedSigner's signature to spend.

## Step 3: Verify a receive address on SeedSigner

Before sending real funds to the new wallet, prove the phone imported *your* keys and not something else:

1. In BlueWallet, open the wallet and tap **Receive** to display an address.
2. On SeedSigner, use the [Address Explorer](/reference/keys/address-explorer.md) (or **Scan** the address QR) to confirm the address belongs to your seed.
3. Only then send funds to it — start small.

> **Warning:** This verification step is what protects you if the phone is compromised. An attacker who tampered with the import would show you *their* addresses — and SeedSigner would refuse to recognize them.

## Step 4: Build a transaction in BlueWallet

When it's time to spend:

1. In BlueWallet, open the wallet, tap **Send**, and enter the recipient and amount.
2. Continue to the signing step. Because the wallet is watch-only, BlueWallet displays the unsigned transaction as an **animated PSBT QR code**.

## Step 5: Sign on SeedSigner, broadcast from the phone

1. On SeedSigner, select **Scan** and read the animated QR from the phone's screen.
2. **Review everything on SeedSigner's screen** — recipient address, amount, fee — exactly as in the [send journey](/get-started/send.md#step-3-review-every-detail--this-is-the-important-part).
3. Approve. SeedSigner displays the signed transaction as a new animated QR.
4. In BlueWallet, scan the **signed transaction** from SeedSigner's screen, then broadcast it.

---

## You're done — checklist

- [ ] Xpub exported from SeedSigner and imported into BlueWallet as watch-only.
- [ ] A receive address **verified on SeedSigner** before funding.
- [ ] A transaction built on the phone, **reviewed and signed on the device**, and broadcast.

## Tips for phone-to-device scanning

Two small screens scanning each other is the fiddliest part of this journey:

- Set **Settings > Advanced > QR Density** to **Low** on SeedSigner so the phone camera locks on faster.
- While a QR is on SeedSigner's screen, push the joystick **up/down** to tune the brightness for the phone's camera.
- Full guide: [QR scanning troubleshooting](/help/qr-scanning.md).

## Where to go next

- [Compatible wallets](/help/compatible-wallets.md) — how BlueWallet compares to Sparrow, Nunchuk, and other coordinators.
- [Send bitcoin](/get-started/send.md) — the desktop version of the same signing flow, in more depth.
- [Set up multisig](/get-started/multisig.md) — combine SeedSigner with other keys for higher security.

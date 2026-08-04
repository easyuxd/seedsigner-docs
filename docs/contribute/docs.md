# Contributing to documentation

> How to run the docs site locally, follow the style guide, and submit changes.

This documentation site is built with [Docsify](https://docsify.js.org/), a lightweight documentation generator that renders Markdown files directly in the browser. There is no build step — you edit Markdown, and the site updates.

---

## Running the site locally

To preview your changes as you write:

1. **Install docsify-cli** (requires Node.js):

   ```bash
   npm i docsify-cli -g
   ```

2. **Serve the site** from the project root:

   ```bash
   docsify serve docs
   ```

3. Open your browser to `http://localhost:3000`. The site auto-reloads when you save changes.

---

## File structure

All documentation lives in the `docs/` folder, organized by section:

```
docs/
├── index.html            # Docsify configuration, theme CSS, diagram styles
├── _sidebar.md           # Sidebar navigation
├── _navbar.md            # Top navigation
├── README.md             # Homepage ("What is SeedSigner?")
├── images/               # All images
├── get-started/          # Goal-based journeys (build, first wallet, send…)
├── reference/            # Screen-first reference, grouped by device aspect
│   ├── hardware/         #   Components, sourcing, assembly, enclosures
│   ├── software/         #   Image verification, flashing, first run
│   ├── device/           #   First boot, navigation, power
│   ├── seeds/            #   Creation, loading, SeedQR, verification, discard
│   ├── keys/             #   Xpub export, address explorer, PSBT signing
│   ├── multisig/         #   Descriptor, multisig spending
│   └── settings/         #   Basic, advanced, hardware settings
├── security/             # Security model, multisig rationale, key storage
├── help/                 # Troubleshooting, FAQ, glossary, resources
└── contribute/           # Contributor docs (you are here)
```

Each section folder contains one Markdown file per page.

---

## Sidebar navigation

The sidebar is defined in `docs/_sidebar.md`. When you add a new page, you need to add a corresponding entry there. Follow the existing format:

```markdown
- **Section Name**
  - [Page title](section-folder/filename.md)
```

---

## Markdown style guide

Follow these conventions to keep the docs consistent:

- **Use headings** (`#`, `##`, `###`) to structure each page. Start with a single `#` heading at the top.
- **Write short paragraphs.** Two to four sentences per paragraph is ideal.
- **Use tables** for structured comparisons or reference data.
- **Use tips and warnings** with this format:

  ```markdown
  > **Tip:** Helpful supplementary information.

  > **Warning:** Important caution the reader should know.
  ```

- **Use code blocks** with language hints for commands and code **only — never for diagrams** (see [Diagrams](#diagrams) below):

  ```markdown
  ```bash
  docsify serve docs
  ```​
  ```

- **Use active voice** and address the reader as "you."

---

## Diagrams

Diagrams are written as **semantic HTML directly in the Markdown**, using the `ss-*` CSS classes defined in `docs/index.html`. They stay fully text-editable, render with the site's brand styling, adapt to mobile, and read correctly in screen readers. Never draw diagrams as ASCII art in code fences.

**Conventions:**

- **Blue = the coordinator** (networked computer), always in the **left** lane.
- **Orange = SeedSigner** (air-gapped device), always in the **right** lane.
- The **dashed line is the air gap**; every QR handoff is a pill sitting on that line with a direction arrow. The line is deliberately **neutral grey, not orange** — it divides the two lanes rather than belonging to either.
- Step numbers must match the page's `## Step N` headings exactly.

**Keep them legible as they grow.** The CSS enforces these, so don't work around them:

- **Lane identity is encoded twice, never more:** the coloured left rule and the coloured step numeral. Do not add a background fill to say the same thing a third time.
- **A `--warn` step is the only filled row in a figure.** That is what makes it read as an exception. If two steps are both critical, the diagram is telling you the page needs restructuring, not a second fill.
- **Body copy stays in ink**, not lane colour. Colour is for the rule, the numeral and the lane label.
- Put secondary detail in a nested `<small>` rather than a longer title — the size and weight drop is what creates the scanning order.

> **Warning:** The entire diagram must be **one contiguous HTML block with no blank lines inside it**, and one blank line before and after it. A blank line makes Docsify's Markdown parser close the HTML block and mangle everything after it. Markdown syntax does not work inside the block — use HTML (`<strong>`, `&mdash;`, `&#8594;`).

**Swimlane template** (two-lane flow with QR handoffs):

```html
<figure class="ss-diagram ss-swimlane" aria-label="One-sentence summary of what the diagram shows">
  <div class="ss-lane-heads">
    <span class="ss-lane-head ss-lane-head--computer">Coordinator <em>networked</em></span>
    <span class="ss-gap-label">Air gap</span>
    <span class="ss-lane-head ss-lane-head--device">SeedSigner <em>air-gapped</em></span>
  </div>
  <ol class="ss-steps">
    <li class="ss-step ss-step--computer"><span class="ss-step-num">1</span><span class="ss-step-body"><span class="ss-lane-tag ss-lane-tag--computer">Coordinator</span>First step, on the computer</span><span class="ss-qr-badge">QR<span aria-hidden="true">&nbsp;&#9658;</span></span></li>
    <li class="ss-step ss-step--device"><span class="ss-step-num">2</span><span class="ss-step-body"><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span>Second step, on the device</span></li>
    <li class="ss-step ss-step--span"><span class="ss-step-num">3</span><span class="ss-step-body">A step involving both sides</span></li>
  </ol>
  <figcaption class="ss-caption">Optional caption stating the diagram's takeaway.</figcaption>
</figure>
```

> **Warning:** The `ss-lane-tag` must go **inside** `ss-step-body`, not beside it. As a sibling it becomes a flex item and sits inline next to the title on mobile, cutting the line length to a few words per row.

**Vertical flow template** (single-column step list). There are no columns to read position from, so every step carries a lane tag, shown at all widths:

```html
<figure class="ss-diagram" aria-label="One-sentence summary of what the diagram shows">
  <ol class="ss-flow">
    <li class="ss-step ss-step--device"><span class="ss-step-num">1</span><span class="ss-step-body"><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span>A step on SeedSigner</span></li>
    <li class="ss-step ss-step--computer"><span class="ss-step-num">2</span><span class="ss-step-body"><span class="ss-lane-tag ss-lane-tag--computer">Sparrow</span>A step in the coordinator</span></li>
    <li class="ss-step ss-step--warn"><span class="ss-step-num">3</span><span class="ss-step-body"><span class="ss-lane-tag ss-lane-tag--computer">Sparrow</span>A critical step<small>Why it matters, in one line</small></span></li>
  </ol>
</figure>
```

**Phase strip template** (a long build broken into labelled phases). The steps are one continuous `1..N` sequence, so they hang off one spine and the phases are bands along it — the `ss-pn` number must match the overall sequence, not restart per phase:

```html
<figure class="ss-diagram ss-phases" aria-label="One-sentence summary of what the diagram shows">
  <div class="ss-phase-spine">
    <div class="ss-phase">
      <span class="ss-phase-kicker">Phase 1</span>
      <strong class="ss-phase-title">Hardware</strong>
      <ol class="ss-phase-steps" start="1">
        <li><span class="ss-pn">1</span><span>First step</span></li>
        <li><span class="ss-pn">2</span><span>Second step</span></li>
      </ol>
    </div>
    <div class="ss-phase ss-phase--critical">
      <span class="ss-phase-kicker">Phase 2 &middot; security-critical</span>
      <strong class="ss-phase-title">Software</strong>
      <ol class="ss-phase-steps" start="3">
        <li><span class="ss-pn">3</span><span>A step where security is decided</span></li>
      </ol>
    </div>
  </div>
  <figcaption class="ss-caption">Optional caption stating the diagram's takeaway.</figcaption>
</figure>
```

**Class reference:**

| Class | Purpose |
|-------|---------|
| `ss-diagram` | `<figure>` wrapper for every diagram — give it a one-sentence `aria-label` |
| `ss-swimlane` + `ss-lane-heads` / `ss-lane-head--computer` / `--device` | Two-lane flow with column headers |
| `ss-gap-label` | The "Air gap" label centred over the channel; positioned absolutely, so its place in the markup doesn't matter |
| `ol.ss-steps` | Two-column step grid with the dashed air-gap line down the middle |
| `ol.ss-flow` | Single-column vertical step list |
| `ss-step` + `--computer` / `--device` / `--span` / `--warn` | One step row: lane, full-width, or warning. `--warn` is the only variant that fills |
| `ss-step--handoff` + `ss-handoff-half--computer` / `--device` | A step where both sides act at once (QR round-trip) |
| `ss-step-num` | Circular step-number badge — keep in sync with the page's headings |
| `ss-step-body` | The step's text; put secondary detail in a nested `<small>` |
| `ss-qr-badge` | QR handoff pill; sits on the air-gap line, arrow shows direction |
| `ss-lane-tag` + `--computer` / `--device` | Lane label. Goes **inside** `ss-step-body`. Hidden on desktop in a swimlane (the column says it); always shown in an `ol.ss-flow` |
| `ss-chip` | Small annotation chip (e.g. `&times;3` for repeated actions) |
| `ss-phases` / `ss-phase-spine` / `ss-phase` / `ss-phase--critical` | Multi-phase strip (see `get-started/build-device.md`) |
| `ss-pn` | Step numeral on the phase spine; numbers run continuously across all phases |
| `ss-arch` | Architecture panel (see the homepage) |
| `ss-caption` | `<figcaption>` takeaway line |
| `ss-sr` | Screen-reader-only text, e.g. to spell out an arrow's meaning |

Preview at desktop **and** narrow width (about 375&nbsp;px) before submitting — `npm test` includes automated checks that diagrams render and don't overflow on mobile.

> **Note:** Diagram text is searchable, but if a search match falls *inside* a diagram block the result snippet may show raw markup. Ranking and links are unaffected — this is a known cosmetic limitation of Docsify's search plugin with inline HTML.

---

## Images

Place all images in the `docs/images/` folder. Reference them in Markdown like this:

```markdown
![Description of the image](images/filename.png)
```

Use descriptive filenames (e.g., `assembly-step-3-camera-ribbon.png`, not `IMG_4521.png`).

> **Most device screenshots are generated, not hand-captured.** They are rendered
> from the SeedSigner emulator by the `docs-screenshots/` pipeline in the site
> repository, against one published testnet seed, so every value on screen matches
> the prose beside it. If a device screenshot is wrong or missing, fix the entry in
> that pipeline's manifest rather than replacing the PNG — a hand-edited file is
> overwritten on the next run. Photos, coordinator-wallet screens, and the camera
> viewports are the exceptions and are kept as-is.

---

## Translations

The existing SeedSigner user guide includes translations in Spanish, French, and other languages. We welcome help expanding translations to cover this new documentation structure. If you'd like to contribute translations, open an issue on GitHub to coordinate with other translators.

---

## Submitting your changes

1. Fork the repository and create a branch for your changes.
2. Make your edits and preview them locally with `docsify serve docs`.
3. Submit a pull request with a brief description of what you changed and why.

> **Tip:** Small, focused pull requests are easier to review and merge. If you're making changes across several pages, consider splitting them into separate PRs.

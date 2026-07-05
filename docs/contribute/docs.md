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
- The **dashed line is the air gap**; every QR handoff is a pill sitting on that line with a direction arrow.
- Step numbers must match the page's `## Step N` headings exactly.

> **Warning:** The entire diagram must be **one contiguous HTML block with no blank lines inside it**, and one blank line before and after it. A blank line makes Docsify's Markdown parser close the HTML block and mangle everything after it. Markdown syntax does not work inside the block — use HTML (`<strong>`, `&mdash;`, `&#8594;`).

**Swimlane template** (two-lane flow with QR handoffs):

```html
<figure class="ss-diagram ss-swimlane" aria-label="One-sentence summary of what the diagram shows">
  <div class="ss-lane-heads">
    <span class="ss-lane-head ss-lane-head--computer">Coordinator <em>networked</em></span>
    <span class="ss-gap-label" aria-hidden="true">&#8646; QR only</span>
    <span class="ss-lane-head ss-lane-head--device">SeedSigner <em>air-gapped</em></span>
  </div>
  <ol class="ss-steps">
    <li class="ss-step ss-step--computer"><span class="ss-step-num">1</span><span class="ss-lane-tag ss-lane-tag--computer">Coordinator</span><span class="ss-step-body">First step, on the computer</span><span class="ss-qr-badge">QR<span aria-hidden="true">&nbsp;&#9658;</span></span></li>
    <li class="ss-step ss-step--device"><span class="ss-step-num">2</span><span class="ss-lane-tag ss-lane-tag--device">SeedSigner</span><span class="ss-step-body">Second step, on the device</span></li>
    <li class="ss-step ss-step--span"><span class="ss-step-num">3</span><span class="ss-step-body">A step involving both sides</span></li>
  </ol>
  <figcaption class="ss-caption">Optional caption stating the diagram's takeaway.</figcaption>
</figure>
```

**Vertical flow template** (single-column step list):

```html
<figure class="ss-diagram" aria-label="One-sentence summary of what the diagram shows">
  <ol class="ss-flow">
    <li class="ss-step ss-step--device"><span class="ss-step-num">1</span><span class="ss-step-body">A step on SeedSigner</span></li>
    <li class="ss-step ss-step--computer"><span class="ss-step-num">2</span><span class="ss-step-body">A step in the coordinator</span></li>
    <li class="ss-step ss-step--warn"><span class="ss-step-num">3</span><span class="ss-step-body">A critical step<small>Why it matters, in one line</small></span></li>
  </ol>
</figure>
```

**Class reference:**

| Class | Purpose |
|-------|---------|
| `ss-diagram` | `<figure>` wrapper for every diagram — give it a one-sentence `aria-label` |
| `ss-swimlane` + `ss-lane-heads` / `ss-lane-head--computer` / `--device` | Two-lane flow with column headers |
| `ol.ss-steps` | Two-column step grid with the dashed air-gap line down the middle |
| `ol.ss-flow` | Single-column vertical step list |
| `ss-step` + `--computer` / `--device` / `--span` / `--warn` | One step card: lane, full-width, or warning styling |
| `ss-step--handoff` + `ss-handoff-half--computer` / `--device` | A step where both sides act at once (QR round-trip) |
| `ss-step-num` | Circular step-number badge — keep in sync with the page's headings |
| `ss-step-body` | The step's text; put secondary detail in a nested `<small>` |
| `ss-qr-badge` | QR handoff pill; sits on the air-gap line, arrow shows direction |
| `ss-lane-tag` + `--computer` / `--device` | Lane chip shown only on mobile, where columns stack |
| `ss-chip` | Small annotation chip (e.g. `&times;3` for repeated actions) |
| `ss-phases` / `ss-phase` / `ss-phase--critical` | Multi-phase strip (see `get-started/build-device.md`) |
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

---

## Translations

The existing SeedSigner user guide includes translations in Spanish, French, and other languages. We welcome help expanding translations to cover this new documentation structure. If you'd like to contribute translations, open an issue on GitHub to coordinate with other translators.

---

## Submitting your changes

1. Fork the repository and create a branch for your changes.
2. Make your edits and preview them locally with `docsify serve docs`.
3. Submit a pull request with a brief description of what you changed and why.

> **Tip:** Small, focused pull requests are easier to review and merge. If you're making changes across several pages, consider splitting them into separate PRs.

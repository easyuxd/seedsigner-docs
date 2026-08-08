# SeedSigner Documentation: Site Repository

This repository contains the **documentation website** for [SeedSigner](https://github.com/SeedSigner/seedsigner), an open-source, air-gapped Bitcoin signing device. It is a content + tooling repo: the published pages, the static-site configuration, and the test/CI harness that keeps them healthy.

> **This is not the SeedSigner firmware.** The device software lives at [SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner). This repo only builds the docs site.

---

## Table of contents

- [What this is](#what-this-is)
- [Tech stack](#tech-stack)
- [Navigation](#navigation)
- [Pinned dependency versions](#pinned-dependency-versions)
- [Repository layout](#repository-layout)
- [Local development](#local-development)
- [Testing](#testing)
- [Continuous integration](#continuous-integration)
- [Deployment](#deployment)
- [Authoring & contributing](#authoring--contributing)
- [Writing style guide](#writing-style-guide)
- [Content overview](#content-overview)
- [Known gaps & TODOs](#known-gaps--todos)
- [License & links](#license--links)

---

## What this is

A [Docsify](https://docsify.js.org/) single-page documentation site. Docsify has **no build step**: it ships a static `index.html` that loads the Docsify runtime from a CDN, then fetches and renders the Markdown files in `docs/` client-side at request time. You edit Markdown, reload, and the site updates.

- **54** Markdown files (52 content pages plus the `_sidebar`/`_404` partials) and **203** images under `docs/`. Most of the images are **generated from the emulator** rather than hand-captured — see [docs-screenshots/](docs-screenshots/README.md).
- Hash-based client-side routing (e.g. `/#/reference/hardware/assembly`). Pre-restructure URLs (e.g. `/#/hardware-build/assembly`) still resolve via a Docsify `alias` redirect map in `index.html`.
- Theming, search, code-copy, pagination, image zoom, collapsible sidebar, and a scroll progress bar — all via Docsify plugins (see below).
- A **fixed top bar** holding the logo and the search field, a **permanent sidebar rail** beneath it, and a **page footer** carrying the outbound project links — see [Navigation](#navigation) for the rules these follow.

## Tech stack

| Layer | Choice | Notes |
|---|---|---|
| Site generator | Docsify v4 | Runtime-rendered, no build pipeline |
| Theme | docsify-themeable (`theme-simple`) | Brand color `#f6851b` (SeedSigner orange) set via CSS vars in `docs/index.html` |
| Hosting target | Static files | `docs/.nojekyll` present → intended for GitHub Pages from the `docs/` folder |
| Runtime deps | jsDelivr CDN | Loaded in `docs/index.html`, **pinned to exact versions** |
| Tests | Playwright (`@playwright/test`) | Smoke tests in `tests/`, run against a live docsify server |
| Dev server | docsify-cli | `docsify serve docs` (live reload) |
| CI | GitHub Actions | `.github/workflows/playwright.yml` |
| Language/tooling | Node.js (LTS), TypeScript (test config only) | CI pins `node-version: lts/*` |
| License | MIT | See `LICENSE` |

### Docsify plugins in use

Configured in [docs/index.html](docs/index.html):

- **search** (bundled with docsify) — full-text search box.
- **zoom-image** (bundled with docsify) — click-to-zoom on images.
- **docsify-copy-code:** "Copy" buttons on code blocks.
- **docsify-pagination:** Previous/Next links, cross-chapter.
- **docsify-sidebar-collapse:** collapsible top-level sidebar sections.
- **docsify-progress:** top scroll-progress bar (honors the theme color).
- **Custom inline plugins**, all in the `$docsify.plugins` array in `index.html`:
  - `navChrome` — relocates the logo, the search field and the sidebar toggle into the fixed top bar, and wires the field's keyboard shortcuts and mobile behaviour.
  - `sidebarCurrent` — records which sidebar row is the current page (see [Navigation](#navigation)).
  - `sidebarSubheadingHeadings` — converts nested sidebar groups without a page link (e.g. *Seeds*, *Hardware*) into non-clickable subheadings.

## Navigation

The nav chrome is direction **"Ledger"** with the **"Signal"** search field, from the design exploration. It is all in `docs/index.html`, in two commented blocks: *Sidebar states* near the top and *Navigation chrome* below the diagram styles.

**The top bar holds exactly two things** — the way home (logo) and the way to search. It is fixed at 64px (56px on mobile), so `topMargin: 80` is set in the Docsify config to keep anchor jumps clear of it. The search field is 480×44 with a neutral grey glyph and an orange focus ring, and takes `⌘K` / `Ctrl K` or `/`. Below 768px the field drops out of the bar as a full-width row behind a search button, and the sidebar becomes a drawer over a dimmed scrim.

**Website / GitHub / Community live in the page footer**, not the bar — which is why `loadNavbar` is off and there is no `_navbar.md`.

**The sidebar has three states, each carried by a different device** so no two can be confused:

| State | Signal | Means |
|---|---|---|
| hover / focus | soft grey field behind the row | you can click this |
| selected | orange label + a 2px orange rule at its left edge | you are here |
| expanded | the chevron, and nothing else | this is open |

Two rules follow. Orange marks exactly two rows — the current page and the top-level section containing it; an expanded section that does *not* contain your page stays ink. And the grey field is only ever hover, so it can sit on a selected row without competing: identity lives in the colour and the rule, never in a fill. This is the same law the `ss-*` diagrams follow (see [Contributing to docs](docs/contribute/docs.md)). A single 1em unit sets the rhythm — between categories, inside an expanded category, and between subgroups.

> **Selected state does not use Docsify's `.active`.** Docsify sets `.active` on the current route's row, but `docsify-sidebar-collapse` reuses it for *"the section you last clicked open"* and moves it there — so expanding a section stole the highlight from the page you were on. The `sidebarCurrent` plugin snapshots Docsify's meaning at `doneEach`, the one moment `.active` is authoritative, into `.ss-here` and `.ss-here-within`; all "you are here" styling keys off those. `.active` is left alone because the collapse plugin needs it to drive expansion.

> **Do not cache DOM nodes across Docsify hooks here.** `docsify-progress` runs `body.innerHTML = body.innerHTML + …` in its own `mounted` hook, and installs itself first — that re-parses the whole body, silently detaching anything captured earlier and destroying Docsify's own drawer bindings. Look elements up at the moment of use and delegate listeners from `document`.

## Pinned dependency versions

All runtime CDN dependencies are pinned to exact versions for reproducibility (no floating `@4` / `@latest` ranges). Update these deliberately in [docs/index.html](docs/index.html).

| Package | Version | Purpose |
|---|---|---|
| docsify | 4.13.1 | Core runtime + search/zoom-image plugins |
| docsify-themeable | 0.9.0 | `theme-simple` stylesheet |
| docsify-copy-code | 2.1.1 | Copy buttons |
| docsify-pagination | 2.10.1 | Prev/next navigation |
| docsify-sidebar-collapse | 1.3.5 | Collapsible sidebar |
| docsify-progress | 1.0.3 | Scroll progress bar |

Dev dependencies (see [package.json](package.json)):

| Package | Range | Purpose |
|---|---|---|
| @playwright/test | ^1.59.1 | Test runner |
| docsify-cli | ^4.4.4 | Local + CI dev server (`docsify serve`) |
| @types/node | ^25.5.2 | Types for the Playwright config |

## Repository layout

```
.
├── docs/                       # The published site (served root)
│   ├── index.html              # Docsify config, theme, nav chrome & sidebar states, CDN tags, custom plugins, alias redirects
│   ├── README.md               # Site HOMEPAGE content (route "/") — NOT this file
│   ├── _sidebar.md             # Sidebar navigation (mirror new pages here)
│   ├── _404.md                 # Custom not-found page
│   ├── .nojekyll               # Tells GitHub Pages to serve files as-is
│   ├── get-started/            # Journeys: build-device, first-wallet, receive, send, recover, multisig, bluewallet (+ landing README)
│   ├── reference/              # Screen/object-first reference, grouped into:
│   │   ├── hardware/           #   components, sourcing, assembly, enclosures
│   │   ├── software/           #   image verification, SD flashing, first-run setup
│   │   ├── device/             #   first boot, navigation, power & restart
│   │   ├── seeds/              #   creation, loading, seedqr, verification, discard
│   │   ├── keys/               #   xpub export, address explorer, PSBT signing
│   │   ├── multisig/           #   wallet descriptor, multisig spending
│   │   └── settings/           #   basic, advanced, hardware settings
│   ├── security/               # Security model, why-multisig, physical, key storage, trade-offs
│   ├── help/                   # Troubleshooting (common issues, errors) + FAQ, glossary, wallets, resources
│   ├── contribute/             # Contributing guides, testnet
│   └── images/                 # All screenshots & photos (203 files) — mostly generated, do not hand-edit
├── docs-screenshots/           # Screenshot pipeline: renders docs/images/ from the emulator
│   ├── fixture.py              #   The canonical testnet seed, PSBT, descriptor, addresses
│   ├── manifest.py             #   Every screen: View + kwargs + output filename
│   ├── generate.py             #   Driver + the --census / --links / --retire checks
│   ├── shim.py                 #   Pi hardware mocks, app on sys.path, run_screen patch
│   ├── live_emulator.py        #   Launches the emulator with the fixture seeds loaded (camera captures)
│   ├── camera_qrs.py           #   Renders the QRs composited into the camera viewports
│   └── COORDINATOR.md          #   Procedure for the hand-captured Sparrow_*.png screens
├── screenshot-audit.md         # The 2026-07 audit: what was wrong with the image library
├── screenshot-regen-plan.md    # How it was fixed, phase by phase
├── tests/                      # Playwright smoke tests
│   ├── docs.spec.ts            #   Site smoke tests (routing, images, sidebar, aliases)
│   └── diagrams.spec.ts        #   ss-* diagram rendering + mobile-overflow guards
├── playwright.config.ts        # Test config (PORT-overridable web server)
├── package.json                # Scripts + dev dependencies
├── .github/workflows/          # CI
│   └── playwright.yml
└── README.md                   # ← You are here (contributor/agent guide)
```

> **Two READMEs, on purpose:** `docs/README.md` is the **site homepage** (the content rendered at route `/`). The file you are reading (`/README.md`) is the **repository guide** for contributors and agents and is what GitHub shows on the project page.

## Local development

**Prerequisites:** Node.js (LTS) and npm.

```bash
# 1. Install dev dependencies (docsify-cli, Playwright, etc.)
npm install

# 2. Serve the docs with live reload
npm start            # → http://localhost:3000  (alias: npm run serve)
```

`npm start` runs `docsify serve docs`. Open `http://localhost:3000`; the site auto-reloads on save. No build/compile step exists.

## Testing

End-to-end smoke tests run real Chromium against a live docsify server (Playwright boots the server automatically via the `webServer` config).

```bash
npm test                         # run the suite
npm run test:report              # open the last HTML report
PORT=4173 npx playwright test    # use a different port if 3000 is taken locally
```

What's covered ([tests/docs.spec.ts](tests/docs.spec.ts)):

- Homepage renders the merged Home title.
- **Homepage hero image loads:** a regression guard for relative image paths (the root page must use `images/…`, not `../images/…`).
- No broken images on the homepage.
- An internal hash route renders its content.
- **A pre-restructure URL still resolves via the alias redirect:** guards the old→new URL map in `index.html`.
- Sidebar navigation works.

And ([tests/diagrams.spec.ts](tests/diagrams.spec.ts)):

- Every diagram page renders exactly one visible `.ss-diagram` figure with a non-empty `aria-label`.
- **ASCII-art regression guard:** no box-drawing/arrow characters may reappear in `pre` blocks.
- Desktop: the first-wallet swimlane lays out as two lanes with step badges 1–8.
- Mobile (375 px): no horizontal page overflow on any diagram page; swimlanes stack to one column with lane chips visible.

**Port note:** the dev/test server defaults to port `3000`. If another local service occupies it, set `PORT` — `playwright.config.ts` reads it for both the server and `baseURL`. In CI, `reuseExistingServer` is off so a clean server is always started.

## Continuous integration

[.github/workflows/playwright.yml](.github/workflows/playwright.yml) runs on push/PR to `main`/`master`:

1. `npm ci` (lockfile-strict install — keep `package-lock.json` in sync).
2. `npx playwright install --with-deps` (browsers).
3. `npx playwright test` (boots docsify on port 3000, runs the suite).
4. Uploads the `playwright-report/` artifact.

Currently CI tests **Chromium only**; Firefox/WebKit/mobile projects exist but are commented out in `playwright.config.ts`.

## Deployment

The site is plain static files. `docs/.nojekyll` indicates it is intended to be published via **GitHub Pages serving the `docs/` folder** (Settings → Pages → Branch `main` / `/docs`). Because routing is hash-based and client-side, any static host works (GitHub Pages, Netlify, S3, etc.) — just serve the `docs/` directory.

## Authoring & contributing

Full guide: [docs/contribute/docs.md](docs/contribute/docs.md). Quick rules:

- **Add a page →** create the Markdown file in the right section folder **and** add a link in [docs/_sidebar.md](docs/_sidebar.md). Match the layer convention: journeys (`get-started/`) use action-voice titles ("Create your first wallet"); reference pages use screen/object-first titles ("Seed creation").
- **One `#` H1 per page**, short paragraphs, active voice, address the reader as "you."
- **Images live in `docs/images/`.** Reference them with a path relative to the *current file's depth*:
  - The root homepage (`docs/README.md`) uses `images/name.png` — **no `../`**.
  - One-level pages (`get-started/`, `security/`, `help/`, `contribute/`) use `../images/name.png`.
  - Two-level pages (`reference/<group>/`, e.g. `reference/seeds/`) use `../../images/name.png`.
  - A wrong relative depth escapes or undershoots the served root and 404s.
- **Moving/renaming a page?** Add an entry to the `alias` map in [docs/index.html](docs/index.html) so the old URL still resolves.
- Use descriptive image filenames (`assembly-step-3-camera-ribbon.png`, not `IMG_4521.png`).
- Keep PRs small and focused; preview locally with `npm start` before submitting.

## Writing style guide

The language contract for the published pages. [docs/contribute/docs.md](docs/contribute/docs.md) is the outside contributor's guide to Markdown mechanics and diagrams; this section is the source of truth for voice, tone, and what belongs on a page.

### Voice

Write as **an experienced peer who has done this and is walking you through it.** Not a manual, not a marketer, not a teacher.

- **Second person, always.** Address the reader as "you." The docs say "we" exactly twice, both in `contribute/`, both speaking *as the project* to contributors. "I" appears only inside quoted UI labels (**I Understand**) and reader-voice FAQ questions ("Can I use a Raspberry Pi with Wi-Fi?").
- **Consequences stated plainly, once.** *"A single wrong or out-of-order word can make your Bitcoin **permanently unrecoverable.**"* No softening, no repetition, no dread.
- **The reader is capable, not expert.** Give the *why* in one clause, then move on.
- **Zero hype.** The corpus contains no *revolutionary, amazing, seamless, cutting-edge,* or *robust*, and no "please." Claims are specific and checkable ("roughly $50", "50 rolls for 12 words") rather than adjectival. Exclamation marks appear six times, every one inside quoted device or tool output — never in the docs' own voice.
- **Limitations are stated, not defended.** [Known trade-offs](docs/security/trade-offs.md) names each criticism in the critic's own words as a heading ("The air gap is security theatre"), then answers it with a `**The concern:** / **The response:**` pair. That honesty is the house style, not a one-off.

### The page contract

1. **One `#` H1**, sentence case. Never a second H1.
2. **A deck line** — a one-sentence blockquote immediately under the H1, roughly 10–20 words, stating what the reader gets: `> Generate a new BIP-39 seed phrase using camera entropy, dice rolls, or manual word selection.` It is the page's promise and it appears on 52 of 52 pages.
3. **An orientation paragraph** before the first `##`: what this is, and when you would want it.
4. **The body**, following the layer's skeleton below.
5. **An exit.** Every page ends by pointing somewhere — *Where to go next*, *What to do next*, *Next step*, or *Related pages*. No page dead-ends.

### Layer contracts

The layers have different jobs and different registers. Match the folder you are writing in.

| Layer | Job | H1 style | Register | Skeleton |
|---|---|---|---|---|
| `get-started/` | Get one goal **done**, end to end | Action — "Send bitcoin" | Warmest; contractions welcome | What you need → The journey at a glance (`ss-*` diagram) → `## Step N: …` → You're done: checklist → Where to go next |
| `reference/` | Answer "what does this screen do" | Screen/object — "Seed creation", "Xpub export" | Neutral, dense, complete | Before you begin → Step-by-step → What happens next / Related pages |
| `security/` | Let the reader judge their own risk | Concept — "Known trade-offs" | Most formal — **this folder uses no contractions at all**, across 3,274 words | Principle → what it does and does not cover |
| `help/` | Fix it now, or look it up | Symptom or term — "Common issues" | Direct, diagnostic | Symptom as `##` → numbered fixes, most likely cause first |
| `contribute/` | Onboard a contributor | Task — "Contributing to documentation" | Collegial; the only place "we" is allowed | Prose plus procedure |

Journeys **link down** into reference; reference pages **link up** to the journey that uses them. Neither duplicates the other: a journey walks the happy path with the screens the reader will actually see and defers the exhaustive option list to reference.

### Sentence and paragraph mechanics

- **Sentences average 13 words.** Past about 30, a sentence is doing two jobs — split it.
- **Paragraphs run 2–4 sentences.** Anything longer becomes a list or a table.
- **Front-load.** The first clause carries the point; qualification follows.
- **Numbered lists are procedures. Bullets are options.** Never mix the two in one list.
- **A procedural step opens with a bolded imperative sentence,** then explains: `1. **Verify your power source.** SeedSigner needs a stable 5V supply with at least 2A…`
- **Tables carry comparisons** — script types, single-sig vs. multisig, settings. Prose that reads like a table should be one.

### Callouts

Three labels, written `> **Label:** text`. The colon goes **inside** the bold (297 uses against 7 outside). Do not invent a fourth label, and never stack two callouts back to back.

| Callout | Use when | Current count |
|---|---|---|
| `> **Warning:**` | Getting this wrong costs money, keys, privacy, or hardware — irreversible actions, network mismatch, backup failure, xpub disclosure | 46 |
| `> **Tip:**` | Optional improvement, shortcut, or pointer to a deeper page. **Never** put a safety-critical fact in a Tip | 65 |
| `> **Note:**` | Neutral clarification with no action attached. Rare by design | 4 |

A bold-lead blockquote with its own name (`> **Why "watch-only"?**`) is reserved for a page-specific aside. Use it sparingly — there are 13 in the whole corpus, each used exactly once.

### Terminology

Canonical spellings. Where pages currently disagree, the form below wins.

| Use | Not | Rule |
|---|---|---|
| **Bitcoin** | | The network, protocol, or something belonging to it: *the Bitcoin network*, *a Bitcoin address* |
| **bitcoin** | BTC | The asset you hold or move: *send bitcoin*, *real bitcoin* |
| **SeedSigner** | the SeedSigner | Usually bare and articleless — "SeedSigner is stateless." *The device* is fine for variety |
| **coordinator** | companion app, host wallet | The networked wallet software. Introduce it once per page, then use it plainly |
| **multisig** | multi-sig | Running text, titles, URLs, sidebar. `multi-signature` is acceptable at first mention in `security/` and the glossary |
| **single-sig** | singlesig | `single-signature` at first mention |
| **testnet / mainnet** | Testnet / Mainnet | Lowercase in prose. Capitalize only when quoting an on-screen value: *Settings → Advanced → Bitcoin Network → Testnet* |
| **xpub** | XPUB | Lowercase in prose; **Xpub** only inside a quoted UI label (*Export Xpub*) |
| **Waveshare** | WaveShare | The vendor's own capitalization |
| **seed phrase**, **SeedQR**, **PSBT**, **BIP-39** | seedphrase, Seed QR, psbt, BIP39 | Hyphenate BIP numbers. Expand an acronym on first use per page, then abbreviate |

The unifying rule: **quote the device verbatim, write everything else in house style.** If the screen says "Export Xpub," the bolded UI label says **Export Xpub** — and the sentence around it says "your xpub."

### Formatting

- **UI labels and menu paths are bold, joined by `→` (U+2192), with the whole path inside one bold span:** `**Settings → Advanced → QR Density**`. Not `>`, not `->`. (97 uses of `→`; the 19 `>` survivors are legacy — see *Known drift*.)
- **Internal links are absolute from the docs root and keep the `.md`:** `[Seed creation](/reference/seeds/creation.md)`. 245 of 249 internal links do this; relative page links break under hash routing.
- **Image paths are relative to the file's own depth** (`images/`, `../images/`, `../../images/`) — the rules are in [Authoring & contributing](#authoring--contributing).
- **Alt text is never empty** — 0 of 312 — and describes the screen, not the file: *"Tools menu with Verify Address highlighted"*, *"Xpub details showing fingerprint, derivation path and xpub"*. The working patterns are `<screen> with <element> highlighted` and `<screen> showing <detail>`; 2–8 words is typical.
- **Backticks are for literal strings only:** address prefixes (`` `bc1q…` `` — the `…` character, not three dots), derivation paths (`` `m/84'/0'/0'` ``), filenames, commands, CSS classes. Never for emphasis.
- **Spaced em dash `—` for the aside** (237 uses); **unspaced en dash `–` for numeric ranges** (`Steps 1–5`).
- **Task lists** `- [ ]` build the *You're done* checklist — one line per verifiable outcome, stated as an accomplished fact: `- [ ] First receive address **verified on SeedSigner**.`
- **`---` between major sections is optional**, but be all-or-nothing within a page.
- **Bold marks the load-bearing phrase; italics mark a true contrast** (*not*, *same*). Never bold a whole sentence.

### Never

- Marketing adjectives, exclamation marks, emoji, or "please."
- "Simply," "just," "easy," "obviously" — they blame the reader when it does not work.
- A safety-critical fact hidden in a Tip, an aside, or a parenthetical. It goes in a Warning or in the body.
- Hedged future tense ("you will want to") where an imperative works ("do this").
- ASCII-art diagrams — use the `ss-*` components ([Diagrams](docs/contribute/docs.md#diagrams)). `npm test` fails if box-drawing characters reappear in a `pre` block.
- A new page missing from [docs/_sidebar.md](docs/_sidebar.md), or a moved page without an `alias` entry.
- Restating a reference page inside a journey. Link to it.

### Known drift

Real inconsistencies in the corpus today. Fix them when you touch the file; do not copy them into new work.

- **`>` instead of `→` in menu paths** — `contribute/testnet.md`, `get-started/bluewallet.md`, `help/common-issues.md`, `help/error-messages.md`, `help/qr-scanning.md`, `reference/keys/message-signing.md`, `reference/seeds/bip85.md`, `reference/settings/hardware.md`.
- **Title Case headings** in `contribute/testnet.md` — the only page not in sentence case.
- **`WaveShare`** in `help/common-issues.md`; **`multi-sig`** throughout `security/` and `help/glossary.md`.
- **"send Bitcoin"** (the asset, so lowercase) in `get-started/first-wallet.md`.
- **Extensionless links** — both in `reference/seeds/creation.md`: `/reference/seeds/dice-entropy` and `/reference/seeds/image-entropy`.

### Before you merge

- [ ] One H1 in sentence case; deck line present, one sentence, under ~20 words.
- [ ] Page ends by pointing somewhere.
- [ ] Structure matches the layer's skeleton.
- [ ] Every Warning is a genuine consequence; no safety-critical fact sits in a Tip.
- [ ] Menu paths use `→`; UI labels match the device's own capitalization.
- [ ] Links absolute and `.md`-suffixed; images at the correct relative depth; alt text on every image.
- [ ] Terminology table respected; nothing in `security/` uses a contraction.
- [ ] Read it aloud. If a sentence needs a breath in the middle, split it.

## Content overview

The site uses a **journey-first** information architecture: goal-based journeys in **Get Started** sit in front of a screen/object-first **Reference** layer. Six top-level sidebar sections:

| Section | Folder | Covers |
|---|---|---|
| Home | `README.md` | Merged intro — what SeedSigner is, why, how it works, and where to start |
| Get Started | `get-started/` | Journeys: build your device, create your first wallet, receive, send, recover, set up multisig (+ a "what do you want to do?" landing page) |
| Reference | `reference/` | Screen/object-first docs grouped into hardware, software, device basics, seeds, keys & transactions, multisig, settings |
| Security | `security/` | Security model, why multisig, physical security, key storage, trade-offs |
| Help & Resources | `help/` | Troubleshooting (common issues, error messages) + FAQ, glossary, compatible wallets, resources |
| Contribute | `contribute/` | Contributing to the project & docs, testnet |

## Known gaps & TODOs

- Images for BlueWallet
- Guides for more coordinators
- Dark mode
- Translations
- Expand testing to walk every route in `_sidebar.md`
- Exhaustive settings reference, generated from (and periodically checked against) the firmware source

## License & links

- **License:** MIT — see [LICENSE](LICENSE).
- **This repo:** https://github.com/easyuxd/seedsigner-docs
- **SeedSigner firmware:** https://github.com/SeedSigner/seedsigner
- **SeedSigner website:** https://seedsigner.com
- **Community (Telegram):** https://t.me/SeedSigner

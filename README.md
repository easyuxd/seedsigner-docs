# SeedSigner Documentation — Site Repository

This repository contains the **documentation website** for [SeedSigner](https://github.com/SeedSigner/seedsigner), an open-source, air-gapped Bitcoin signing device. It is a content + tooling repo: the published pages, the static-site configuration, and the test/CI harness that keeps them healthy.

> **This is not the SeedSigner firmware.** The device software lives at [SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner). This repo only builds the docs site.

---

## Table of contents

- [What this is](#what-this-is)
- [Tech stack](#tech-stack)
- [Pinned dependency versions](#pinned-dependency-versions)
- [Repository layout](#repository-layout)
- [Local development](#local-development)
- [Testing](#testing)
- [Continuous integration](#continuous-integration)
- [Deployment](#deployment)
- [Authoring & contributing](#authoring--contributing)
- [Content overview](#content-overview)
- [Known gaps & TODOs](#known-gaps--todos)
- [License & links](#license--links)

---

## What this is

A [Docsify](https://docsify.js.org/) single-page documentation site. Docsify has **no build step**: it ships a static `index.html` that loads the Docsify runtime from a CDN, then fetches and renders the Markdown files in `docs/` client-side at request time. You edit Markdown, reload, and the site updates.

- **54** Markdown files (51 content pages plus the `_sidebar`/`_navbar`/`_404` partials) and **143** images under `docs/`.
- Hash-based client-side routing (e.g. `/#/reference/hardware/assembly`). Pre-restructure URLs (e.g. `/#/hardware-build/assembly`) still resolve via a Docsify `alias` redirect map in `index.html`.
- Theming, search, code-copy, pagination, image zoom, collapsible sidebar, and a scroll progress bar — all via Docsify plugins (see below).

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
- **docsify-copy-code** — "Copy" buttons on code blocks.
- **docsify-pagination** — Previous/Next links, cross-chapter.
- **docsify-sidebar-collapse** — collapsible top-level sidebar sections.
- **docsify-progress** — top scroll-progress bar (honors the theme color).
- **Custom inline plugin** (`sidebarSubheadingHeadings`) — converts nested sidebar groups without a page link (e.g. *Seeds*, *Hardware*) into non-clickable subheadings. Lives in the `$docsify.plugins` array in `index.html`.

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
│   ├── index.html              # Docsify config, theme, CDN script tags, custom plugin, alias redirects
│   ├── README.md               # Site HOMEPAGE content (route "/") — NOT this file
│   ├── _sidebar.md             # Sidebar navigation (mirror new pages here)
│   ├── _navbar.md              # Top navbar links
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
│   └── images/                 # All screenshots & photos (143 files)
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

`npm start` runs `docsify serve docs`. Open `http://localhost:3000`; the site auto-reloads on save. No build/compile step exists — what you edit is what ships.

## Testing

End-to-end smoke tests run real Chromium against a live docsify server (Playwright boots the server automatically via the `webServer` config).

```bash
npm test                         # run the suite
npm run test:report              # open the last HTML report
PORT=4173 npx playwright test    # use a different port if 3000 is taken locally
```

What's covered ([tests/docs.spec.ts](tests/docs.spec.ts)):

- Homepage renders the merged Home title.
- **Homepage hero image loads** — a regression guard for relative image paths (the root page must use `images/…`, not `../images/…`).
- No broken images on the homepage.
- An internal hash route renders its content.
- **A pre-restructure URL still resolves via the alias redirect** — guards the old→new URL map in `index.html`.
- Sidebar navigation works.

And ([tests/diagrams.spec.ts](tests/diagrams.spec.ts)):

- Every diagram page renders exactly one visible `.ss-diagram` figure with a non-empty `aria-label`.
- **ASCII-art regression guard** — no box-drawing/arrow characters may reappear in `pre` blocks.
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

> ⚠️ **No automated deploy is configured yet.** The only workflow is CI tests; publishing is manual. See [Known gaps](#known-gaps--todos).

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

Honest list of what's incomplete or worth improving, ranked roughly by importance. Items 1–4 are the outstanding recommendations from the 2026-07 comprehensive audit (the audit's higher-ranked items — the `ss-*` diagram system and the ecosystem content gap-fill: QR scanning guide, GPG verification walkthrough, BlueWallet journey, SettingsQR / BIP-85 / message signing / dice entropy pages, Pi variant comparison, boot-time note — are done).

1. **No deploy automation.** Add a GitHub Actions workflow that publishes `docs/` to GitHub Pages on every push to `main`. Today the only workflow is CI tests; publishing is manual.
2. **Site-wide link/image crawl test.** Extend Playwright beyond the current smoke tests: walk **every** route in `_sidebar.md`, assert no 404s and no broken images on any page, and assert every entry in the `alias` redirect map resolves. This protects the IA/restructure investment against silent link rot.
3. **Dark mode.** Add a `prefers-color-scheme: dark` override of the docsify-themeable CSS variables in `docs/index.html`. The diagram system is already fully variable-driven (`--ss-*` tokens), so diagrams inherit dark mode for free once the token block is overridden.
4. **Lower-priority audit items:**
   - **CDN sourcing.** Runtime deps are pinned but still loaded from jsDelivr at request time. Vendor the assets locally and/or add Subresource Integrity (SRI) hashes for stronger reproducibility/offline support.
   - **Browser coverage.** CI tests Chromium only; the Firefox/WebKit/mobile projects exist but are commented out in `playwright.config.ts`.
   - **Content gap — assembly photos.** `reference/hardware/assembly.md` would benefit from a "components laid out before assembly" photo. Needs a real photograph.
   - **Translations.** The legacy SeedSigner user guide had multi-language translations; this restructured site does not yet. Contributions welcome (coordinate via a GitHub issue).
5. **Future content idea.** An exhaustive settings reference generated from (and periodically checked against) the firmware source — exact menu paths and every option value, kept in sync per SeedSigner release.
6. **Platform note (not an action item).** The audit's verdict was to **stay on Docsify** — revisit a migration (e.g. Astro Starlight: non-hash URLs, prerendered HTML for SEO, built-in dark mode/i18n) only if SEO or translations become priorities. Mermaid support was likewise deliberately skipped in favor of the hand-styled `ss-*` diagrams; if contributors ever need ad-hoc diagrams, it can be added with a small `markdown.renderer.code` hook in `index.html`.
7. **Dev-dependency advisories.** `npm audit` reports advisories in the transitive `docsify-cli` tree (dev/build-time only — never shipped to the static site). Revisit when upstream updates.

## License & links

- **License:** MIT — see [LICENSE](LICENSE).
- **This repo:** https://github.com/easyuxd/seedsigner-docs
- **SeedSigner firmware:** https://github.com/SeedSigner/seedsigner
- **SeedSigner website:** https://seedsigner.com
- **Community (Telegram):** https://t.me/SeedSigner

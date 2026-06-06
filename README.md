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

- **45** Markdown files (content pages plus the `_sidebar`/`_navbar`/`_404` partials) and **143** images under `docs/`.
- Hash-based client-side routing (e.g. `/#/hardware-build/assembly`).
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
- **Custom inline plugin** (`sidebarSubheadingHeadings`) — converts nested sidebar groups without a page link (e.g. *Build*, *Seeds*) into non-clickable subheadings. Lives in the `$docsify.plugins` array in `index.html`.

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
│   ├── index.html              # Docsify config, theme, CDN script tags, custom plugin
│   ├── README.md               # Site HOMEPAGE content (route "/") — NOT this file
│   ├── _sidebar.md             # Sidebar navigation (mirror new pages here)
│   ├── _navbar.md              # Top navbar links
│   ├── _404.md                 # Custom not-found page
│   ├── .nojekyll               # Tells GitHub Pages to serve files as-is
│   ├── overview.md
│   ├── getting-started/        # Quick-start checklist, first boot, navigation, power
│   ├── hardware-build/         # Components, sourcing, assembly, enclosures
│   ├── software-setup/         # Download/verify, write SD card, first run
│   ├── using-seedsigner/       # Seeds, keys/wallets, transactions
│   ├── security/               # Security model + multi-sig guides
│   ├── configuration/          # Settings reference
│   ├── troubleshooting/        # Common issues, error messages
│   ├── appendices/             # FAQ, glossary, compatible wallets, resources
│   ├── development/            # Contributing guides, testnet
│   └── images/                 # All screenshots & photos (143 files)
├── tests/                      # Playwright smoke tests
│   └── docs.spec.ts
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

- Homepage renders the documentation title.
- **Homepage hero image loads** — a regression guard for relative image paths (the root page must use `images/…`, not `../images/…`).
- No broken images on the homepage.
- An internal hash route renders its content.
- Sidebar navigation works.

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

Full guide: [docs/development/contributing-docs.md](docs/development/contributing-docs.md). Quick rules:

- **Add a page →** create the Markdown file in the right section folder **and** add a link in [docs/_sidebar.md](docs/_sidebar.md).
- **One `#` H1 per page**, short paragraphs, active voice, address the reader as "you."
- **Images live in `docs/images/`.** Reference them with a path relative to the *current* file:
  - Pages inside a section folder (e.g. `using-seedsigner/`) use `../images/name.png`.
  - The root homepage (`docs/README.md`) uses `images/name.png` — **no `../`** (that escapes the served root and 404s).
- Use descriptive image filenames (`assembly-step-3-camera-ribbon.png`, not `IMG_4521.png`).
- Keep PRs small and focused; preview locally with `npm start` before submitting.

## Content overview

| Section | Folder | Covers |
|---|---|---|
| Getting Started | `getting-started/` | Quick-start checklist, first boot, navigation, power off |
| Hardware Build | `hardware-build/` | Components list, sourcing, assembly, enclosures |
| Software Setup | `software-setup/` | Download & verify, write SD card, first-run config |
| Using SeedSigner | `using-seedsigner/` | Beginner single-sig walkthrough, create/load/back-up/view/discard seeds, xpub export, addresses, signing PSBTs |
| Security & Multi-sig | `security/` | Security model, physical security, key storage, trade-offs, multi-sig setup/spend/descriptor |
| Configuration | `configuration/` | Basic, advanced, and hardware settings |
| Troubleshooting | `troubleshooting/` | Common issues, error messages |
| Reference | `appendices/` | FAQ, glossary, compatible wallets, resources |
| Development | `development/` | Contributing to the project & docs, testnet |

## Known gaps & TODOs

Honest list of what's incomplete or worth improving:

- **No deploy automation.** Add a GitHub Pages (or other) deploy workflow so merges publish automatically. Today it is manual.
- **Smoke-test depth.** The suite is intentionally shallow (5 tests). Candidates: crawl every sidebar route, verify no broken internal links/images site-wide, add a11y checks, and enable mobile/Firefox/WebKit projects.
- **Content gap — assembly photos.** `hardware-build/assembly.md` would benefit from a "components laid out before assembly" photo (previously a stray inline TODO, now removed). Track as a content task with a real screenshot.
- **CDN sourcing.** Runtime deps are pinned but still loaded from jsDelivr at request time. For stronger reproducibility/offline support, consider vendoring the assets locally and/or adding Subresource Integrity (SRI) hashes.
- **Dev-dependency advisories.** `npm audit` reports advisories in the transitive `docsify-cli` tree (dev/build-time only — never shipped to the static site). Revisit when upstream updates.
- **Translations.** The legacy SeedSigner user guide had multi-language translations; this restructured site does not yet. Contributions welcome (coordinate via a GitHub issue).

## License & links

- **License:** MIT — see [LICENSE](LICENSE).
- **This repo:** https://github.com/easyuxd/seedsigner-docs
- **SeedSigner firmware:** https://github.com/SeedSigner/seedsigner
- **SeedSigner website:** https://seedsigner.com
- **Community (Telegram):** https://t.me/SeedSigner

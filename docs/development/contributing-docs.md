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
├── index.html            # Docsify configuration
├── _sidebar.md           # Sidebar navigation
├── overview.md           # "What is SeedSigner?"
├── images/               # All images
├── getting-started/      # Getting started guides
├── hardware-build/       # Hardware build guide
├── software-setup/       # Software setup
├── using-seedsigner/     # Core usage guides
├── security/             # Security and multi-sig
├── configuration/        # Settings reference
├── troubleshooting/      # Troubleshooting
├── development/          # Development docs (you are here)
└── appendices/           # FAQ, glossary, resources
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

- **Use code blocks** with language hints for commands and code:

  ```markdown
  ```bash
  docsify serve docs
  ```​
  ```

- **Use active voice** and address the reader as "you."

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

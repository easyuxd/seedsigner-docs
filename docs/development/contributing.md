# Contributing to SeedSigner

> How to contribute code, testing, documentation, translations, and bug reports to the project.

SeedSigner is a fully open-source project released under the [MIT License](https://github.com/SeedSigner/seedsigner/blob/dev/LICENSE). Contributions from the community are what keep it moving forward.

**GitHub repository:** [github.com/SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner)

---

## Ways to contribute

There are many ways to get involved beyond writing code:

- **Code** — Fix bugs, add features, or improve performance. The codebase is Python.
- **Testing** — Run development builds on your hardware and report what works (and what doesn't).
- **Documentation** — Improve guides, fix typos, or write new content. See [Contributing to docs](/development/contributing-docs.md).
- **Translations** — Help make SeedSigner accessible to more people around the world.
- **Bug reports** — Found something broken? File a clear, detailed issue on GitHub.
- **Enclosure designs** — Design and share 3D-printable cases or other hardware enclosures.

---

## Development setup

To work on SeedSigner code locally:

1. **Fork and clone the repository.**

   ```bash
   git clone https://github.com/YOUR-USERNAME/seedsigner.git
   cd seedsigner
   ```

2. **Set up a Python environment.** SeedSigner is written in Python. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the test suite** to make sure everything is working before you make changes.

4. **Use testnet for testing.** Never test transaction-signing workflows with real bitcoin. See [Using testnet](/development/testnet.md) for setup instructions.

---

## Submitting changes

1. **Create a feature branch** off the `dev` branch (not `main`).

   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b your-feature-name
   ```

2. **Make your changes** in small, focused commits with clear commit messages.

3. **Submit a pull request** against the `dev` branch on GitHub. Include a description of what your change does and why.

> **Warning:** Pull requests submitted against `main` instead of `dev` will need to be retargeted. Always branch from and PR into `dev`.

---

## Filing issues

If you find a bug or want to suggest a feature:

1. Search [existing issues](https://github.com/SeedSigner/seedsigner/issues) first to avoid duplicates.
2. Open a new issue with a clear title and detailed description.
3. For bugs, include your SeedSigner version, hardware details, and steps to reproduce.
4. For feature requests, describe the use case and why it would be valuable.

---

## Community

The SeedSigner community is active on **Telegram**. Join the channel to ask questions, discuss development, share ideas, and connect with other contributors.

> **Tip:** If you're not sure where to start, look for issues labeled "good first issue" on GitHub. These are specifically chosen as approachable entry points for new contributors.

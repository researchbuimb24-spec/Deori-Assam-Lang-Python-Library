# Contributing to `deori`

Thank you for your interest in contributing to `deori`!

This library exists to serve community members, learners, linguists, and NLP developers working with the Deori (Deuri) language. To protect the integrity of documentation for an endangered language, we maintain strict standards for both code and linguistic data.

---

## 1. Golden Rules for Linguistic Data

1. **NEVER invent or hypothesize words, morphemes, or sentences.**
   - Every single lexical entry, inflectional affix, and example sentence must originate from a verified, documented source or directly from confirmed native speaker consultation.
   - If an entry lacks specific citation, mark it as `TODO: needs source`.
2. **Every data record requires provenance.**
   - Include `source` (author, publication year, page/section number or recording ID).
   - Include `variety` (e.g. `dibongiya`, `tengapaniya`, `borgonya`, `patorgonya`, or `unspecified`).
3. **Record conflicts; do not resolve them arbitrarily.**
   - If Brown (1895) reports one form and Jacquesson (2005) or Deori Sahitya Sabha reports another, document both with respective citations.
4. **Community Guidance is Paramount.**
   - We actively defer to the Deori Sahitya Sabha and native speakers for orthographic and linguistic decisions. This library is an assistant, not an authority over native speakers.

---

## 2. Development Setup

The project uses modern Python packaging via `uv` or standard virtual environments (`>= Python 3.10`).

```bash
# Clone the repository
git clone https://github.com/researchbuimb24-spec/Deori-Assam-Lang-Python-Library.git
cd Deori-Assam-Lang-Python-Library

# Create a virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

---

## 3. Code Standards & Testing

All contributions must pass automated linting, type-checking, and test suites:

- **Formatting & Linting**: `ruff format` and `ruff check`
- **Type Checking**: `mypy --strict` with zero warnings or errors.
- **Testing**: `pytest --cov=deori` with at least 90% test coverage.
- **Property-based Testing**: Transliteration and normalization modules must include `hypothesis` test suites verifying round-trip invariants and Unicode stability.
- **Unicode Rigor**: Always ensure NFC normalization (`unicodedata.normalize("NFC", text)`), proper handling of Assamese script codepoints (ৰ U+09F0 vs র U+09B0, ৱ U+09F1 vs ব U+09AC), and proper preservation of virama and zero-width joiners/non-joiners.

---

## 4. Submitting Pull Requests

1. Fork the repo and create your feature branch: `git checkout -b feature/orthography-assamese`
2. Ensure all tests and linters pass:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run mypy
   uv run pytest
   ```
3. Commit with concise, descriptive commit messages.
4. Open a Pull Request referencing the relevant milestone or issue.

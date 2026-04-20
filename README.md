# CryptoLab

<p align="center">
  <a>
    <img src="https://img.shields.io/badge/Python-3.10+-3178C6?style=for-the-badge&logo=python&logoColor=white&labelColor=2D3748" alt="Python 3.10+" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=2D3748" alt="Framework: Streamlit" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Cryptography-pycryptodome%20%7C%20cryptography-4A90D9?style=for-the-badge&labelColor=2D3748" alt="Cryptography: pycryptodome and cryptography" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Classical%20Ciphers-pycipher%20%7C%20secretpy-7B68EE?style=for-the-badge&labelColor=2D3748" alt="Classical: pycipher and secretpy" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Visualization-Plotly-3D9970?style=for-the-badge&logo=plotly&logoColor=white&labelColor=2D3748" alt="Visualization: Plotly" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/version-1.1.0-blue?style=for-the-badge&labelColor=2D3748" alt="Version: 1.1.0" />
  </a>
</p>

<p align="center">
  <a>
    <img src="https://img.shields.io/badge/Algorithms-25+-informational?style=flat-square&labelColor=2D3748" alt="Algorithms: 25+" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Categories-7-9B59B6?style=flat-square&labelColor=2D3748" alt="Categories: 7" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Classical%20Ciphers-14-E67E22?style=flat-square&labelColor=2D3748" alt="Classical Ciphers: 14" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Platform-Web%20App-2C3E50?style=flat-square&labelColor=2D3748" alt="Platform: Web" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square&labelColor=2D3748" alt="Status: In Development" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/License-MIT-6C5CE7?style=flat-square&labelColor=2D3748" alt="License: MIT" />
  </a>
</p>

> An interactive, modular cryptography learning platform built with Streamlit. Experiment with 25+ real library-backed algorithms spanning the full history of cryptography — from Ancient Roman Caesar ciphers to modern AES-256-GCM and ChaCha20-Poly1305. Visualize transformations, compare outputs, process files in batch, and understand the why behind every algorithm.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Algorithm Coverage](#algorithm-coverage)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Tabs](#tabs)
- [Plugin System](#plugin-system)
- [Technologies Used](#technologies-used)
- [Design Principles](#design-principles)
- [Limitations](#limitations)
- [Future Scope](#future-scope)
- [License](#license)
- [Author](#author)

---

## Overview

CryptoLab is an educational cryptography platform that lets users experiment hands-on with real, production-quality cryptographic algorithms — not textbook pseudocode or hand-rolled toy implementations. Every cipher, hash function, and encoding utility is backed by a reputable Python library, verified with roundtrip tests before release.

The platform spans the full arc of cryptographic history:

- **Classical era** — Caesar (~50 BC), Atbash (~600 BC), Scytale (~700 BC), Vigenere (1553), Playfair (1854), and more. All broken by modern standards, all included to show *why* modern cryptography had to be invented.
- **Legacy modern** — Blowfish, Triple DES. Still encountered in older systems; clearly labeled.
- **Modern secure** — AES-256-GCM, ChaCha20-Poly1305, RSA-OAEP, Fernet. What you should actually use.
- **Hash functions** — MD5 through SHA-3 and BLAKE2, with honest strength labels.
- **Authentication** — HMAC with configurable digest algorithms.
- **Encoding utilities** — Base64, Base32, Hex, URL encoding, Binary. Clearly distinguished from encryption.
- **Secure randomness** — Cryptographically secure token generation via Python's `secrets` module.

The app is built with Streamlit and runs entirely in a web browser with no external services, no database, and no API keys required.

### Key Features (Quick Overview)

- 25+ algorithms across 7 categories, all library-backed
- Lab workbench with dynamic per-algorithm settings panels
- Transformation pipeline visualization for each operation
- Multi-algorithm comparison with timing, output size, and entropy charts
- Batch file processing (.txt upload)
- Learn tab with JSON-driven algorithm metadata, concept explainers, and English letter frequency analysis
- Session history with JSON export
- Favorites and recently used tracking
- Modular plugin architecture — add or remove algorithms without touching the core app

---

## Features

### Lab
- Algorithm selector with category filter and search
- Dynamic settings panel per algorithm — key size, cipher mode, Affine a/b, Bifid period, Caesar shift slider, and more
- Operations: Encrypt, Decrypt, Hash, Compute MAC, Encode/Decode, Generate
- Strength indicator and warning banner for legacy, weak, and historical algorithms
- Transformation pipeline visualization showing every processing step
- Output text area with download and key reveal
- Favorites (save button) and recently used sidebar sections
- Per-run session history entry
- Full input validation with user-friendly error messages

### Compare
- Enter one input, select any number of algorithms, run all simultaneously
- Result cards with output preview, category, strength, timing, and char count
- Plotly charts: execution time, output size, and output entropy side by side
- Export comparison results as JSON

### Batch Mode
- Upload a `.txt` file and process its full contents with any batch-capable algorithm
- Covers all symmetric ciphers, classical ciphers, hash functions, HMAC, and encoding
- Auto-generated key display when key field is left blank (for decrypt-later workflows)
- Preview of first 500 characters, then download full result

### Learn
- Algorithm cards sourced from `data/*.json` metadata files
- Per-card fields: creator, era introduced, key sizes, modern use, breakability, notes, Did You Know
- Direct links: Wikipedia and Google search per algorithm
- Strength and search filters
- Core concept explainers:
  - Encryption vs Hashing vs Encoding
  - Symmetric vs Asymmetric Encryption
  - Why MD5 and SHA-1 are broken
  - Authenticated Encryption (AEAD)
  - History of Classical Ciphers (Atbash to Bifid)
  - English letter frequency chart (Plotly) — visualises why monoalphabetic ciphers fail

### History
- Full session operation log: algorithm, operation, input preview, output preview, timing
- Expandable detail per entry
- Export entire history as JSON
- Clear history button

### About
- Version, algorithm count, category count
- Full tech stack breakdown
- Plugin development guide with code examples
- Classical vs Modern cipher comparison table
- Design principles

---

## Algorithm Coverage

### Modern Encryption

| Algorithm | Library | Key Sizes | Mode | Strength |
|---|---|---|---|---|
| AES | pycryptodome | 128 / 192 / 256-bit | GCM, EAX, CBC | Secure |
| Fernet | cryptography | 256-bit total (AES-128 + HMAC-128) | AES-CBC + HMAC-SHA256 | Secure |
| RSA | pycryptodome | 1024 / 2048 / 4096-bit | OAEP / SHA-256 | Secure |
| ChaCha20-Poly1305 | pycryptodome | 256-bit | AEAD stream cipher | Secure |

### Legacy Encryption

| Algorithm | Library | Key Sizes | Strength |
|---|---|---|---|
| Blowfish | pycryptodome | 32–448-bit (CBC) | Legacy |
| Triple DES (3DES) | pycryptodome | 112–168-bit (CBC) | Legacy |

### Hashing — 12 Algorithms

| Algorithm | Output | Strength |
|---|---|---|
| MD5 | 128-bit | Weak — collision attacks known |
| SHA-1 | 160-bit | Weak — SHAttered collision (2017) |
| SHA-224 / 256 / 384 / 512 | 224–512-bit | Secure |
| SHA3-224 / 256 / 384 / 512 | 224–512-bit | Secure (Keccak sponge) |
| BLAKE2b / BLAKE2s | 256–512-bit | Secure |

All via `hashlib` (Python stdlib). Output in hex or base64.

### Authentication

| Algorithm | Digest Options | Library | Strength |
|---|---|---|---|
| HMAC | SHA-256, SHA-512, SHA3-256, SHA-1 (weak), MD5 (weak) | hmac (stdlib) | Secure |

### Encoding — 11 Operations

Base64 Encode/Decode · Base32 Encode/Decode · Hex Encode/Decode · URL Encode/Decode · Binary Encode/Decode · ROT13

All via Python stdlib (`base64`, `binascii`, `urllib.parse`, `codecs`). Not encryption — clearly labeled.

### Randomness

| Tool | Output Types | Library |
|---|---|---|
| Secure Token Generator | Hex, URL-safe Base64, Raw Bytes (b64), Numeric PIN, Passphrase, API Key | secrets (stdlib) |

### Classical Ciphers — Educational Only

All 14 ciphers backed by `pycipher` or `secretpy`. Zero hand-rolled algorithm logic.

| Cipher | Type | Library | Era |
|---|---|---|---|
| Caesar | Monoalphabetic Substitution | pycipher | Ancient Rome ~50 BC |
| ROT13 | Monoalphabetic Substitution | pycipher | Internet era |
| Atbash | Monoalphabetic Substitution | pycipher | Ancient Hebrew ~600 BC |
| Affine | Monoalphabetic Substitution | pycipher | 16th century |
| Simple Substitution | Monoalphabetic Substitution | pycipher | Classical antiquity |
| Keyword Substitution | Monoalphabetic Substitution | secretpy | Medieval |
| Vigenere | Polyalphabetic Substitution | pycipher | 1553 — Bellaso |
| Beaufort | Polyalphabetic Substitution | pycipher | 19th century — Beaufort |
| Autokey | Polyalphabetic Substitution | pycipher | 1586 — de Vigenere |
| Gronsfeld | Polyalphabetic Substitution | pycipher | 17th century |
| Playfair | Polygraphic Substitution | pycipher | 1854 — Wheatstone |
| Bifid | Polygraphic Substitution | pycipher | 1901 — Delastelle |
| Railfence | Transposition | pycipher | American Civil War |
| Scytale | Transposition | secretpy | Ancient Sparta ~700 BC |

> Classical ciphers accept alphabetic input only. Numbers, spaces, and punctuation are preserved unchanged. Playfair treats J as I and separates double-letter pairs with X — correct per historical specification.

---

## Project Structure

```
CryptoLab/
│
├── app.py                          # Entry point — tabs imported and rendered here
│
├── .streamlit/
│   └── config.toml                 # Dark Professional theme settings
│
├── algorithms/                     # Plugin modules — one file per algorithm family
│   ├── aes_tool.py                 # AES-128/192/256 (GCM, EAX, CBC)
│   ├── fernet_tool.py              # Fernet (AES-128-CBC + HMAC-SHA256)
│   ├── rsa_tool.py                 # RSA-OAEP / SHA-256 (keypair generation included)
│   ├── chacha20_tool.py            # ChaCha20-Poly1305 AEAD
│   ├── blowfish_tool.py            # Blowfish-CBC (legacy)
│   ├── tripledes_tool.py           # Triple DES-CBC (legacy)
│   ├── hash_tool.py                # SHA family + BLAKE2 + MD5 (12 algorithms)
│   ├── hmac_tool.py                # HMAC with configurable digest algorithm
│   ├── encoding_tool.py            # Base64/32, Hex, URL, Binary, ROT13
│   ├── token_tool.py               # Secure token generation (secrets stdlib)
│   └── classical_tool.py           # 14 classical ciphers (pycipher + secretpy)
│
├── core/
│   ├── registry.py                 # Discovers and registers algorithm modules at startup
│   ├── engine.py                   # Dispatches operations to modules; measures timing
│   └── metadata.py                 # Loads and caches JSON metadata files
│
├── data/                           # JSON metadata (one file per algorithm family)
│   ├── aes.json
│   ├── fernet.json
│   ├── rsa.json
│   ├── chacha20.json
│   ├── hash.json
│   ├── hmac.json
│   ├── encoding.json
│   ├── token.json
│   └── classical.json
│
├── tabs/                           # UI tab modules
│   ├── home.py                     # Landing page, category overview, Did You Know facts
│   ├── lab.py                      # Main crypto workbench (settings, run, output, viz)
│   ├── compare.py                  # Multi-algorithm comparison with Plotly charts
│   ├── batch.py                    # .txt file upload and batch processing
│   ├── learn.py                    # Algorithm deep-dives, concept explainers, freq chart
│   ├── history.py                  # Session operation log with JSON export
│   └── about.py                    # Tech stack, plugin guide, design notes
│
├── utils/
│   ├── theme_css.py                # Dark Professional CSS injection (design tokens)
│   ├── ui_helpers.py               # Badges, pipeline visualizer, output boxes
│   ├── validators.py               # Text and file input validation
│   ├── text_tools.py               # Shannon entropy, character frequency, byte utils
│   └── file_ops.py                 # File read helpers for batch mode
│
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ybs294000/cryptolab.git
cd cryptolab

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

No configuration files, secrets, or external services are required.

### Dependencies

```
streamlit>=1.35.0
cryptography>=42.0.0
pycryptodome>=3.20.0
plotly>=5.18.0
pycipher>=0.9.0
secretpy>=0.11.0
```

### Platform Compatibility

CryptoLab has no OS-specific dependencies and runs on any platform Python supports.

| Environment | Status |
|---|---|
| Windows 10 / 11 | Tested |
| Ubuntu 24.04 LTS | Tested |
| macOS | Expected to work |
| Streamlit Cloud | Deployable |
| Modern browsers (Chrome, Firefox, Edge) | Supported |

---

## Usage

### Encrypt and Decrypt (Lab Tab)

1. Go to the **Lab** tab
2. Select an algorithm (e.g. AES, Fernet, ChaCha20)
3. Select **Encrypt** operation
4. Configure settings — leave the key field blank to auto-generate
5. Enter your plaintext and click **Run**
6. Copy or download the output. Save the key shown under "Key used" to decrypt later
7. Switch operation to **Decrypt**, paste the ciphertext, enter the saved key, click **Run**

### Hash Text

1. Go to **Lab**, select **Hash Functions**
2. Choose a hash algorithm (SHA-256 recommended)
3. Enter text and click **Run**
4. View the digest and entropy of the output
5. Expand the Hash Size Comparison chart to compare digest lengths across all algorithms

### Classical Ciphers

1. Go to **Lab**, select **Classical Ciphers**
2. Choose a cipher from the dropdown — the era and category are shown below
3. Enter the key for the selected cipher (shift for Caesar, keyword for Vigenere, etc.)
4. Enter your text and click **Run**
5. Switch to Decrypt and run with the same key to recover the original

### Comparing Algorithms

1. Go to the **Compare** tab
2. Enter input text
3. Select two or more algorithms from the multiselect
4. Click **Compare**
5. Review output cards and execution time, output size, and entropy charts
6. Export as JSON

### Batch Processing

1. Go to the **Batch** tab
2. Select an algorithm and operation
3. Configure key settings (or leave blank)
4. Upload a `.txt` file
5. Click **Process File** — preview the result and download

### Learning

1. Go to the **Learn** tab
2. Browse algorithm cards by category or use the search and strength filters
3. Expand any card for history, key sizes, modern use, breakability, notes, and external links
4. Scroll to the Concepts section for explainers on AEAD, SHA-1 being broken, classical cipher history, and the English letter frequency chart

---

## Tabs

| Tab | Description |
|---|---|
| **Home** | Platform overview, algorithm category cards, Did You Know facts, quick start guide |
| **Lab** | Main workbench — algorithm selector, settings panel, run, output, pipeline visualization |
| **Compare** | Side-by-side multi-algorithm comparison with Plotly timing, size, and entropy charts |
| **Batch** | Upload `.txt` files for bulk processing with any supported algorithm |
| **Learn** | JSON-driven algorithm cards, concept explainers, letter frequency chart |
| **History** | Session operation log (algorithm, op, previews, timing) with JSON export |
| **About** | Tech stack, architecture overview, plugin development guide |

---

## Plugin System

Each algorithm is a self-contained module in `algorithms/`. Adding a new cipher requires no changes to the core app.

### 1. Create `algorithms/my_algo.py`

```python
ID = "my_algo"
NAME = "My Algorithm"
CATEGORY = "Modern Encryption"      # Used for grouping in UI
DESCRIPTION = "Short description."
STRENGTH = "secure"                 # secure | legacy | weak | none | historical
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["symmetric", "modern"]

def default_settings() -> dict:
    return {"key": "", "mode": "GCM"}

def validate_settings(settings: dict) -> tuple[bool, str]:
    ...

# Implement whichever operations apply:
def encrypt(plaintext: str, settings: dict) -> dict: ...
def decrypt(ciphertext: str, settings: dict) -> dict: ...
def hash_text(plaintext: str, settings: dict) -> dict: ...
def encode(text: str, settings: dict) -> dict: ...
def generate(_, settings: dict) -> dict: ...
def compute_hmac(message: str, settings: dict) -> dict: ...

# Optional — enables pipeline visualization in Lab tab:
def get_visualization_steps(plaintext: str, settings: dict) -> list[tuple[str, str]]: ...
```

All operation functions return `{"output": "..."}` on success or `{"error": "..."}` on failure. Optional extra keys: `key_used`, `info`, `elapsed_ms`.

### 2. Register in `core/registry.py`

Add one line to the `imports` list inside `_build_registry()`:

```python
("algorithms.my_algo", "encrypt/decrypt"),
```

The algorithm appears in all tabs automatically. If the library is unavailable, the module is skipped silently and the app continues running normally.

### 3. Optional extras

- **Metadata**: Create `data/my_algo.json` (fields: `id`, `name`, `description`, `notes`, `did_you_know`, `wikipedia_url`, etc.) — it appears in the Learn tab automatically.
- **Settings UI**: Add an `elif algo_entry["id"] == "my_algo":` block in `_get_settings_panel()` in `tabs/lab.py` for a custom settings panel. Without this, the algorithm runs with `default_settings()`.

---

## Technologies Used

| Category | Technology |
|---|---|
| UI Framework | Streamlit >= 1.35 |
| Modern Encryption | cryptography >= 42.0, pycryptodome >= 3.20 |
| Hashing / HMAC / Secure Tokens | hashlib, hmac, secrets (Python stdlib) |
| Encoding | base64, binascii, urllib.parse, codecs (Python stdlib) |
| Classical Ciphers | pycipher >= 0.9, secretpy >= 0.11 |
| Visualization | Plotly >= 5.18 |
| Theme | Custom Dark Professional CSS (design tokens via CSS variables) |

---

## Design Principles

**No hand-rolled cryptography.** Every algorithm uses a reputable, actively maintained library. Modern ciphers use `cryptography` and `pycryptodome`. Classical ciphers use `pycipher` and `secretpy`. There is no manual implementation of AES, RSA, Caesar, Vigenere, Playfair, or any other algorithm in this codebase.

**Graceful degradation.** If a library fails to import, the algorithm module is skipped and the app continues running. Every other algorithm remains available.

**Authenticated encryption by default.** For symmetric encryption, AEAD modes (GCM, EAX, Poly1305) are the default. These protect both confidentiality and integrity — if the ciphertext is tampered with, decryption fails with an explicit error.

**Honest strength labeling.** Every algorithm carries one of: `SECURE`, `LEGACY`, `WEAK`, `ENCODING`, or `HISTORICAL / BROKEN`. Classical ciphers always display a warning banner. MD5 and SHA-1 are marked `WEAK`. Blowfish and 3DES are marked `LEGACY`.

**Roundtrip verified.** All encrypt/decrypt pairs — AES (GCM, EAX, CBC), Fernet, ChaCha20, Blowfish, 3DES, RSA, and all 14 classical ciphers — are unit-tested. Keys exported as base64 are accepted back on the key input field for decryption.

**Clean plugin architecture.** Adding or removing an algorithm touches exactly two files. All tabs discover algorithms from the registry at runtime with no hardcoded lists.

---

## Limitations

- Classical ciphers process alphabetic characters only. Numbers, spaces, and punctuation are passed through unchanged and not encrypted.
- Playfair treats J as I and separates double-letter pairs with X per the historical specification. Decrypted output may contain X separators not present in the original plaintext — this is expected behavior.
- RSA encryption is limited by key size. A 2048-bit key can encrypt at most ~190 bytes of plaintext. For larger data, use hybrid encryption (RSA to exchange an AES key, then AES for bulk data).
- Symmetric ciphers with auto-generated keys (blank key field) display the key after the operation. This key is not persisted anywhere and must be saved manually to decrypt later.
- Hash functions are one-way — there is no decryption operation.
- Encoding (Base64, Hex, URL, etc.) provides no security and is trivially reversible.
- All operations run in the browser session. No data is sent to any external server or service.
- Maximum input size is 512 KB for both text and file operations.

---

## Future Scope

- Add elliptic-curve cryptography (ECDH, ECDSA) via the `cryptography` library
- Add password hashing (bcrypt, scrypt, Argon2) with security comparison and timing benchmarks
- Add a live frequency analysis attack demo against Caesar and Vigenere ciphertext
- Add character frequency chart as a live output panel in the Lab tab
- Add Columnar Transposition and Enigma machine simulation (pycipher supports both)
- Support binary file batch processing (not just `.txt`)
- Add diff view between plaintext and ciphertext — highlight which characters changed
- Persistent favorites and history across sessions
- Exportable PDF report per operation
- Multilingual UI support

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute it with attribution.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Yash Shah**
- GitHub: [@ybs294000](https://github.com/ybs294000)
- Email: yashbshah2004@gmail.com

---

*Built with Streamlit · No external services required · Runs entirely in your browser*
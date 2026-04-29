# CryptoLab

CryptoLab is a Streamlit-based cryptography lab for learning, comparing, and testing real library-backed algorithms. It covers modern encryption, legacy ciphers, hashing, HMAC, encoding, secure token generation, and classical ciphers for education.

The app now also includes a secure file workflow for protecting common binary files such as images, PDFs, and spreadsheets with authenticated encryption.

## Highlights

- Lab tab for one-algorithm-at-a-time experimentation
- Compare tab with timing, output length, and entropy views
- Batch text processing for `.txt` files
- Secure File Vault for encrypting and decrypting common binary files
- Learn tab with JSON-driven metadata and concept explainers
- Study tab with JSON-driven quizzes and flashcards rendered from a schema file
- Session history, saved algorithms, and recent activity
- Shared logo branding and dark professional UI theme
- Automated tests with generated fixtures and markdown test reports

## Supported Algorithm Families

- Modern encryption: AES, Fernet, RSA, ChaCha20-Poly1305
- Legacy encryption: Blowfish, Triple DES
- Hashing: MD5, SHA-1, SHA-2, SHA-3, BLAKE2
- Authentication: HMAC
- Encoding: Base64, Base32, Hex, URL, Binary, ROT13
- Randomness: secure token generator
- Historical ciphers: Caesar, Vigenere, Playfair, Scytale, and more

## Secure File Vault

The Batch tab now has a separate secure file workflow for binary files.

Recommended file-protection choices:

- AES-GCM
- ChaCha20-Poly1305
- Fernet

How it works:

1. Upload a file such as `png`, `jpg`, `pdf`, `xlsx`, `docx`, `csv`, or similar
2. Choose a protection algorithm
3. Encrypt the file into a `.cryptolab` secure package
4. Save the generated key if one is auto-created
5. Decrypt the package later to restore the original file name and bytes

## Project Structure

```text
CryptoLab/
├── app.py
├── algorithms/
├── assets/
├── core/
├── data/
│   └── study/
├── docs/
├── tabs/
├── tests/
├── utils/
├── .streamlit/config.toml
├── CHANGELOG.md
├── README.md
└── requirements.txt
```

## Installation

Requirements:

- Python 3.10+
- pip

Install and run:

```bash
git clone https://github.com/ybs294000/cryptolab.git
cd cryptolab
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Dependencies

```text
streamlit>=1.35.0
cryptography>=42.0.0
pycryptodome>=3.20.0
plotly>=5.18.0
pycipher==0.5.2
secretpy>=0.11.0
```

## Testing

Fixture generation:

```bash
python tests\generate_sample_files.py
```

Run the suite and regenerate the report:

```bash
python tests\run_tests.py
```

Latest report:

```text
tests/TEST_REPORT.md
```

See also:

- [docs/TESTING.md](docs/TESTING.md)
- [docs/THEMING.md](docs/THEMING.md)
- [CHANGELOG.md](CHANGELOG.md)

## Design Notes

- No hand-rolled cryptography for modern or classical algorithms
- Authenticated encryption is preferred for real file protection
- Legacy and weak algorithms are clearly labeled
- Historical ciphers are included for learning, not real-world security
- UI theme is coordinated through `.streamlit/config.toml` and `utils/theme_css.py`
- Study Mode reads its quizzes, flashcards, and layout rules from `data/study/`

## Current Limits

- Maximum input and upload size is 512 KB
- RSA is not available in batch file mode because of plaintext size constraints
- History and saved state are session-based, not persisted across reloads
- Classical ciphers operate on alphabetic text only

## Author

Yash Shah  
GitHub: [@ybs294000](https://github.com/ybs294000)

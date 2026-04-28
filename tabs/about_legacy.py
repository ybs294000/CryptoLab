"""
Legacy technical About tab content preserved for reference.
"""

import streamlit as st
from core.registry import get_all, get_by_category

APP_VERSION = "1.1.0"


def render() -> None:
    st.markdown("### About CryptoLab")

    all_algos = get_all()
    cats = get_by_category()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Version", APP_VERSION)
    col2.metric("Algorithm Families", len(all_algos))
    col3.metric("Categories", len(cats))
    col4.metric("License", "MIT")

    st.markdown("---")

    st.markdown("""
CryptoLab is an educational cryptography platform built with Streamlit. It provides
a hands-on interface to experiment with real cryptographic algorithms using reputable
Python libraries.

**Purpose**: Learn how cryptographic algorithms work by using them directly.
Every operation uses production-quality or well-vetted library code.
No algorithms are hand-implemented from scratch.

The platform spans the full history of cryptography - from Ancient Rome's Caesar
cipher through WW2-era Enigma precursors, to modern authenticated encryption
like AES-256-GCM and ChaCha20-Poly1305.
""")

    st.markdown("---")
    st.markdown("### Algorithm Coverage")

    for cat_name, entries in cats.items():
        names = ", ".join(e["name"] for e in entries)
        st.markdown(f"**{cat_name}** — {names}")

    st.markdown("---")
    st.markdown("### Tech Stack")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**UI Framework**
- Streamlit >= 1.35

**Modern Cryptography**
- `cryptography` - Fernet, AES-GCM
- `pycryptodome` - AES, ChaCha20-Poly1305, Blowfish, 3DES, RSA-OAEP
- `hashlib` (stdlib) - SHA-1/2/3 family, BLAKE2, MD5
- `hmac` (stdlib) - HMAC-SHA256/512
- `secrets` (stdlib) - Cryptographically secure tokens
- `base64`, `binascii`, `urllib.parse` (stdlib) - Encoding
""")
    with col_b:
        st.markdown("""
**Classical Ciphers (Educational)**
- `pycipher` - Caesar, Vigenere, Atbash, Affine, ROT13,
  Beaufort, Autokey, Gronsfeld, Playfair, Bifid,
  Railfence, Simple Substitution
- `secretpy` - Scytale, Keyword Substitution

**Visualization**
- Plotly - timing charts, entropy, output size comparison

**Architecture**
- Modular algorithm plugin system
- JSON-driven metadata / Learn tab
- Central registry + engine dispatcher
- Session-state history tracking
""")

    st.markdown("---")
    st.markdown("### How to Add an Algorithm")

    with st.expander("Plugin Development Guide"):
        st.markdown("""
Each algorithm is a standalone Python module in the `algorithms/` directory.

**1. Create `algorithms/my_algo.py`**

Your module should expose:

```python
ID = "my_algo"
NAME = "My Algorithm"
CATEGORY = "Modern Encryption"
DESCRIPTION = "Short description."
STRENGTH = "secure"  # secure | legacy | weak | none | historical
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["symmetric", "modern"]

def default_settings() -> dict: ...
def validate_settings(settings: dict) -> tuple[bool, str]: ...

# Implement the operations you support:
def encrypt(plaintext: str, settings: dict) -> dict: ...
def decrypt(ciphertext: str, settings: dict) -> dict: ...
# or hash_text / encode / generate / compute_hmac

# Optional - for pipeline visualization:
def get_visualization_steps(plaintext: str, settings: dict) -> list[tuple[str, str]]: ...
```

**2. Register it in `core/registry.py`**

Add the import path to the `imports` list in `_build_registry()`.

**3. Add metadata (optional)**

Create `data/my_algo.json` with id, name, category, description, notes, did_you_know, wikipedia_url fields.

**4. Add settings UI (optional)**

Add an `elif algo_entry["id"] == "my_algo":` block in `_get_settings_panel()` in `tabs/lab.py`.
Otherwise the algorithm runs with `default_settings()`.
""")

    st.markdown("---")
    st.markdown("### Design Principles")

    with st.expander("Implementation Rules"):
        st.markdown("""
- **No hand-rolled crypto**: Every algorithm uses a reputable library.
  Modern ciphers use `cryptography`/`pycryptodome`. Classical ciphers use `pycipher`/`secretpy`.
- **Graceful degradation**: If a library is unavailable the algorithm is skipped - the app keeps running.
- **Authenticated encryption by default**: Where possible, AEAD modes (GCM, EAX, Poly1305) are the default.
- **Clear strength labeling**: Legacy, weak, and historical algorithms are prominently marked. No security theater.
- **Educational honesty**: Classical ciphers are shown as historical/broken, never as secure alternatives.
- **Roundtrip verified**: All encrypt/decrypt pairs are unit-tested before release.
""")

    with st.expander("Classical vs Modern Ciphers"):
        st.markdown("""
CryptoLab includes both classical (historical) and modern ciphers. They serve very different purposes:

| | Classical | Modern |
|---|---|---|
| Era | 50 BC - 1940s | 1970s - present |
| Security | Broken | Secure |
| Key space | Tiny (Caesar: 25 keys) | Vast (AES-256: 2^256 keys) |
| Attack | Frequency analysis, pen+paper | Requires nation-state compute (if any) |
| Use today | Education, puzzles, CTF | TLS, disk encryption, VPNs |

The classical ciphers are included to illustrate how cryptography evolved and why modern algorithms were needed.
""")

    st.markdown("---")
    st.markdown("### Run Command")
    st.code("streamlit run app.py", language="bash")
    st.caption("Requires Python 3.10+ and the packages in requirements.txt")

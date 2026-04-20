# CryptoLab

An educational cryptography learning platform built with Streamlit.

## Features

- **Lab** - Experiment with 10 algorithm families (AES, Fernet, RSA, ChaCha20, 3DES, Blowfish, SHA family, HMAC, encoding, token generation)
- **Compare** - Run the same input through multiple algorithms and compare outputs, timing, and entropy
- **Batch** - Process entire .txt files with any algorithm
- **Learn** - Detailed information about each algorithm: history, strengths, weaknesses, modern use
- **History** - Session operation history with JSON export

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

```
CryptoLab/
  app.py                  Main entry point
  requirements.txt
  .streamlit/
    config.toml           Dark theme config
  algorithms/             One module per algorithm (plugin system)
    aes_tool.py
    fernet_tool.py
    rsa_tool.py
    chacha20_tool.py
    blowfish_tool.py
    tripledes_tool.py
    hash_tool.py
    hmac_tool.py
    encoding_tool.py
    token_tool.py
  core/
    registry.py           Auto-discovers algorithm modules
    engine.py             Dispatches operations to modules
    metadata.py           Loads JSON metadata files
  data/                   JSON metadata per algorithm
  tabs/                   One file per UI tab
  utils/                  Shared helpers
```

## Adding Algorithms

1. Create `algorithms/my_algo.py` - expose ID, NAME, CATEGORY, STRENGTH, and operation functions
2. Add the module path to `core/registry.py` imports list
3. Optionally create `data/my_algo.json` metadata

## Libraries Used

- `cryptography` - Fernet, AES-GCM
- `pycryptodome` - AES, ChaCha20-Poly1305, Blowfish, 3DES, RSA-OAEP
- `hashlib` (stdlib) - SHA-1/2/3, BLAKE2, MD5
- `hmac` (stdlib) - HMAC
- `secrets` (stdlib) - Cryptographically secure tokens
- `plotly` - Charts and comparisons

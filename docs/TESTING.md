# Testing

CryptoLab uses a small `unittest` suite that exercises both core helpers and the secure file workflow.

## What is covered

- Registry loading and algorithm availability
- Branding asset availability
- Secure package metadata roundtrip
- Input and upload validation
- Binary and document encryption/decryption roundtrips for:
  - AES-GCM
  - ChaCha20-Poly1305
  - Fernet
- Text API roundtrips after binary support was added

## Test fixtures

Fixtures are generated automatically into `tests/fixtures/` and include:

- A copied PNG logo from `assets/logo1.png`
- A sample text file
- A generated sample PDF
- A generated sample XLSX workbook
- A binary payload

## Commands

Generate or refresh fixtures:

```bash
python tests\generate_sample_files.py
```

Run the full suite and regenerate the markdown report:

```bash
python tests\run_tests.py
```

## Report output

The latest report is written to:

```text
tests/TEST_REPORT.md
```

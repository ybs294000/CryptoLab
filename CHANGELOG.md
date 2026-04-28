# Changelog

## 1.2.0 - 2026-04-27

- Added shared logo-based branding for the sidebar and major page headers
- Reworked the About tab into a more user-facing experience
- Preserved the previous technical About content in `tabs/about_legacy.py`
- Added a secure file vault workflow in the Batch tab
- Added authenticated encryption support for binary files using:
  - AES-GCM
  - ChaCha20-Poly1305
  - Fernet
- Added secure package helpers for encrypted file export/import
- Added fixture generation and a `unittest` suite for core helpers and secure file roundtrips
- Added markdown test report generation in `tests/TEST_REPORT.md`
- Added `a_tmp/` and `tmp/` as ignored local scratch folders
- Refined the UI theme to match the dark professional reference more closely
- Simplified the page background to remove the distracting shell gradient
- Corrected the installable `pycipher` version in `requirements.txt`

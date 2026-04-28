"""
File I/O helpers for CryptoLab.
"""

import json


def read_uploaded_text(uploaded_file) -> tuple[bool, str, str]:
    """
    Read an uploaded Streamlit file as text.
    Returns (success, content_or_error, encoding_used).
    """
    try:
        raw = uploaded_file.read()
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                return True, raw.decode(enc), enc
            except UnicodeDecodeError:
                continue
        return False, "Could not decode file with common encodings.", ""
    except Exception as e:
        return False, f"File read error: {e}", ""


def prepare_download_text(content: str) -> bytes:
    return content.encode("utf-8")


def prepare_download_bytes(content: bytes) -> bytes:
    return content


def read_uploaded_bytes(uploaded_file) -> tuple[bool, bytes | str]:
    try:
        return True, uploaded_file.getvalue()
    except Exception as e:
        return False, f"File read error: {e}"


def build_secure_file_package(
    *,
    algorithm_id: str,
    algorithm_settings: dict | None = None,
    original_name: str,
    media_type: str,
    encrypted_output: str,
) -> bytes:
    payload = {
        "format": "cryptolab-secure-file",
        "version": 2,
        "algorithm_id": algorithm_id,
        "algorithm_settings": algorithm_settings or {},
        "original_name": original_name,
        "media_type": media_type or "application/octet-stream",
        "encrypted_output": encrypted_output,
    }
    return json.dumps(payload, indent=2).encode("utf-8")


def parse_secure_file_package(raw_bytes: bytes) -> tuple[bool, dict | str]:
    try:
        payload = json.loads(raw_bytes.decode("utf-8"))
    except Exception as e:
        return False, f"Package parse failed: {e}"

    required = {"format", "version", "algorithm_id", "encrypted_output"}
    if not required.issubset(payload.keys()):
        return False, "This file is not a valid CryptoLab secure package."
    if payload.get("format") != "cryptolab-secure-file":
        return False, "Unsupported secure package format."
    if "algorithm_settings" not in payload or not isinstance(payload.get("algorithm_settings"), dict):
        payload["algorithm_settings"] = {}
    return True, payload

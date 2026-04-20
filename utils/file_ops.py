"""
File I/O helpers for CryptoLab.
"""

import io


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

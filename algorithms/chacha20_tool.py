"""
ChaCha20-Poly1305 AEAD encryption using PyCryptodome.
"""

import base64
import os
from Crypto.Cipher import ChaCha20_Poly1305

ID = "chacha20"
NAME = "ChaCha20-Poly1305"
CATEGORY = "Modern Encryption"
DESCRIPTION = "Fast stream cipher with Poly1305 authentication. 256-bit key. Preferred on mobile/embedded."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["modern", "stream cipher", "authenticated", "fast"]


def default_settings() -> dict:
    return {"key": ""}


def validate_settings(settings: dict) -> tuple[bool, str]:
    key = settings.get("key", "").strip()
    if key and len(key.encode()) != 32:
        return False, "ChaCha20 requires exactly 32 bytes (32 ASCII characters) key."
    return True, ""


def _get_key(settings: dict) -> bytes:
    """
    Key resolution order:
    1. _key_bytes (raw bytes stored by encrypt for same-session decrypt)
    2. key field as base64 (from key_used export)
    3. key field as UTF-8 text padded/truncated to 32 bytes
    4. random (auto-generate)
    """
    import base64 as _b64

    raw = settings.get("_key_bytes")
    if isinstance(raw, bytes) and len(raw) == 32:
        return raw

    key = settings.get("key", "").strip()
    if not key:
        return os.urandom(32)

    # Try base64 decode first (key_used output is base64)
    try:
        decoded = _b64.b64decode(key)
        if len(decoded) == 32:
            return decoded
    except Exception:
        pass

    # Fall back to UTF-8 pad/truncate
    kb = key.encode("utf-8")
    return (kb + b"\x00" * 32)[:32]


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        cipher = ChaCha20_Poly1305.new(key=key)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
        nonce = cipher.nonce
        combined = nonce + tag + ciphertext
        encoded = base64.b64encode(combined).decode()
        key_b64 = base64.b64encode(key).decode()
        # Store raw key bytes so a same-call decrypt helper can reuse it
        settings["_key_bytes"] = key
        return {
            "output": encoded,
            "key_used": key_b64,
            "info": f"Key (base64): {key_b64}  (paste into Key field to decrypt)",
        }
    except Exception as e:
        return {"error": f"ChaCha20 encrypt failed: {e}"}


def decrypt(ciphertext_b64: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        combined = base64.b64decode(ciphertext_b64.strip())
        nonce = combined[:12]
        tag = combined[12:28]
        ct = combined[28:]
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        return {"output": plaintext.decode("utf-8")}
    except Exception as e:
        return {"error": f"ChaCha20 decrypt failed: {e}"}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = encrypt(plaintext, settings)
    if "error" in result:
        return []
    return [
        ("Plaintext", plaintext),
        ("256-bit Key + Nonce", result.get("key_used", "")[:32] + "..."),
        ("ChaCha20 Keystream XOR", "[stream cipher XOR operation]"),
        ("Poly1305 Auth Tag", "[16-byte MAC appended]"),
        ("Final Encoded Output", result["output"]),
    ]

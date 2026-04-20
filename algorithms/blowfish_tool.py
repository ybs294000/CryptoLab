"""
Blowfish encryption using PyCryptodome.
Marked legacy - superseded by AES.
"""

import base64
import os
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad

ID = "blowfish"
NAME = "Blowfish"
CATEGORY = "Legacy Encryption"
DESCRIPTION = "Symmetric block cipher by Bruce Schneier (1993). 32-448 bit keys. Superseded by AES."
STRENGTH = "legacy"
SUPPORTS_VISUALIZATION = False
SUPPORTS_BATCH_MODE = True
TAGS = ["legacy", "symmetric", "block cipher"]


def default_settings() -> dict:
    return {"key": ""}


def validate_settings(settings: dict) -> tuple[bool, str]:
    key = settings.get("key", "").strip()
    if key:
        kb = key.encode("utf-8")
        if len(kb) < 4 or len(kb) > 56:
            return False, "Blowfish key must be 4-56 bytes."
    return True, ""


def _get_key(settings: dict) -> bytes:
    import base64 as _b64
    key = settings.get("key", "").strip()
    if not key:
        return os.urandom(16)
    try:
        decoded = _b64.b64decode(key)
        if 4 <= len(decoded) <= 56:
            return decoded
    except Exception:
        pass
    return key.encode("utf-8")[:56]


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        bs = Blowfish.block_size
        cipher = Blowfish.new(key, Blowfish.MODE_CBC)
        padded = pad(plaintext.encode("utf-8"), bs)
        ciphertext = cipher.encrypt(padded)
        combined = cipher.iv + ciphertext
        encoded = base64.b64encode(combined).decode()
        return {
            "output": encoded,
            "key_used": base64.b64encode(key).decode(),
            "info": f"Key (base64): {base64.b64encode(key).decode()} [LEGACY - prefer AES]",
        }
    except Exception as e:
        return {"error": f"Blowfish encrypt failed: {e}"}


def decrypt(ciphertext_b64: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        bs = Blowfish.block_size
        combined = base64.b64decode(ciphertext_b64.strip())
        iv = combined[:bs]
        ct = combined[bs:]
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ct), bs)
        return {"output": plaintext.decode("utf-8")}
    except Exception as e:
        return {"error": f"Blowfish decrypt failed: {e}"}

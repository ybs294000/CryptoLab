"""
Triple DES (3DES) encryption using PyCryptodome.
Legacy - superseded by AES.
"""

import base64
import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

ID = "tripledes"
NAME = "Triple DES (3DES)"
CATEGORY = "Legacy Encryption"
DESCRIPTION = "Applies DES cipher three times. 112-168 bit security. Superseded by AES. Still found in legacy banking systems."
STRENGTH = "legacy"
SUPPORTS_VISUALIZATION = False
SUPPORTS_BATCH_MODE = True
TAGS = ["legacy", "symmetric", "block cipher"]


def default_settings() -> dict:
    return {"key": ""}


def validate_settings(settings: dict) -> tuple[bool, str]:
    return True, ""


def _get_key(settings: dict) -> bytes:
    import base64 as _b64
    key = settings.get("key", "").strip()
    if not key:
        while True:
            k = os.urandom(24)
            try:
                DES3.adjust_key_parity(k)
                return k
            except ValueError:
                continue
    # Accept base64 key (from key_used export)
    try:
        decoded = _b64.b64decode(key)
        if len(decoded) == 24:
            return DES3.adjust_key_parity(decoded)
        if len(decoded) == 16:
            decoded = decoded + decoded[:8]
            return DES3.adjust_key_parity(decoded)
    except Exception:
        pass
    kb = key.encode("utf-8")
    if len(kb) < 16:
        kb = kb.ljust(16, b"\x00")
    if len(kb) < 24:
        kb = kb[:16] + kb[:8]
    kb = kb[:24]
    try:
        return DES3.adjust_key_parity(kb)
    except ValueError:
        return os.urandom(24)


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        cipher = DES3.new(key, DES3.MODE_CBC)
        padded = pad(plaintext.encode("utf-8"), DES3.block_size)
        ciphertext = cipher.encrypt(padded)
        combined = cipher.iv + ciphertext
        encoded = base64.b64encode(combined).decode()
        return {
            "output": encoded,
            "key_used": base64.b64encode(key).decode(),
            "info": f"Key (base64): {base64.b64encode(key).decode()} [LEGACY - prefer AES]",
        }
    except Exception as e:
        return {"error": f"3DES encrypt failed: {e}"}


def decrypt(ciphertext_b64: str, settings: dict) -> dict:
    try:
        key = _get_key(settings)
        combined = base64.b64decode(ciphertext_b64.strip())
        iv = combined[:8]
        ct = combined[8:]
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ct), DES3.block_size)
        return {"output": plaintext.decode("utf-8")}
    except Exception as e:
        return {"error": f"3DES decrypt failed: {e}"}

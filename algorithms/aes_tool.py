"""
AES encryption/decryption using PyCryptodome.
Supports AES-128, AES-192, AES-256 in CBC, GCM, EAX modes.
"""

import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

ID = "aes"
NAME = "AES"
CATEGORY = "Modern Encryption"
DESCRIPTION = "Advanced Encryption Standard - symmetric block cipher (128/192/256-bit keys)."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["modern", "symmetric", "block cipher"]

KEY_SIZES = {
    "AES-128": 16,
    "AES-192": 24,
    "AES-256": 32,
}

MODES = ["CBC", "GCM", "EAX"]


def default_settings() -> dict:
    return {
        "key_size": "AES-256",
        "mode": "GCM",
        "key": "",
    }


def validate_settings(settings: dict) -> tuple[bool, str]:
    key = settings.get("key", "").strip()
    key_size = settings.get("key_size", "AES-256")
    required = KEY_SIZES.get(key_size, 32)
    if key and len(key.encode()) != required:
        return False, f"{key_size} requires exactly {required} bytes ({required} ASCII characters)."
    return True, ""


def _derive_key(settings: dict) -> bytes:
    import base64 as _b64
    key = settings.get("key", "").strip()
    key_size = settings.get("key_size", "AES-256")
    required = KEY_SIZES.get(key_size, 32)
    if not key:
        return os.urandom(required)
    # Accept base64-encoded key (from key_used output)
    try:
        decoded = _b64.b64decode(key)
        if len(decoded) == required:
            return decoded
    except Exception:
        pass
    kb = key.encode("utf-8")
    if len(kb) < required:
        kb = kb.ljust(required, b"\x00")
    return kb[:required]


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        key = _derive_key(settings)
        mode_name = settings.get("mode", "GCM")
        data = plaintext.encode("utf-8")

        if mode_name == "GCM":
            cipher = AES.new(key, AES.MODE_GCM)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            nonce = cipher.nonce
            combined = nonce + tag + ciphertext
            encoded = base64.b64encode(combined).decode()
        elif mode_name == "EAX":
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            nonce = cipher.nonce
            combined = nonce + tag + ciphertext
            encoded = base64.b64encode(combined).decode()
        else:  # CBC
            cipher = AES.new(key, AES.MODE_CBC)
            padded = pad(data, AES.block_size)
            ciphertext = cipher.encrypt(padded)
            combined = cipher.iv + ciphertext
            encoded = base64.b64encode(combined).decode()

        return {
            "output": encoded,
            "key_used": base64.b64encode(key).decode(),
            "mode": mode_name,
            "info": f"Key: {base64.b64encode(key).decode()}  (save this to decrypt)",
        }
    except Exception as e:
        return {"error": f"AES encrypt failed: {e}"}


def decrypt(ciphertext_b64: str, settings: dict) -> dict:
    try:
        key = _derive_key(settings)
        mode_name = settings.get("mode", "GCM")
        combined = base64.b64decode(ciphertext_b64.strip())

        if mode_name == "GCM":
            nonce = combined[:16]
            tag = combined[16:32]
            ct = combined[32:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ct, tag)
        elif mode_name == "EAX":
            nonce_len = 16
            nonce = combined[:nonce_len]
            tag = combined[nonce_len:nonce_len + 16]
            ct = combined[nonce_len + 16:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ct, tag)
        else:  # CBC
            iv = combined[:16]
            ct = combined[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(ct), AES.block_size)

        return {"output": plaintext.decode("utf-8")}
    except Exception as e:
        return {"error": f"AES decrypt failed: {e}. Check your key and mode."}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = encrypt(plaintext, settings)
    if "error" in result:
        return []
    return [
        ("Plaintext", plaintext),
        ("UTF-8 bytes", plaintext.encode("utf-8").hex()),
        (f"AES-{settings.get('mode','GCM')} Encrypted", result["output"][:60] + "..."),
        ("Base64 Encoded Output", result["output"]),
    ]

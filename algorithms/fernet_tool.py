"""
Fernet symmetric encryption using the cryptography library.
Fernet guarantees authenticated encryption (AES-128-CBC + HMAC-SHA256).
"""

import base64
from cryptography.fernet import Fernet, InvalidToken

ID = "fernet"
NAME = "Fernet"
CATEGORY = "Modern Encryption"
DESCRIPTION = "Symmetric authenticated encryption using AES-128-CBC + HMAC-SHA256. Simple, secure, and hard to misuse."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["modern", "symmetric", "authenticated"]

MODES = ["Encrypt", "Decrypt"]


def default_settings() -> dict:
    return {"key": ""}


def validate_settings(settings: dict) -> tuple[bool, str]:
    key = settings.get("key", "").strip()
    if key:
        try:
            Fernet(key.encode())
        except Exception:
            return False, "Invalid Fernet key. Generate one with the button below."
    return True, ""


def generate_key() -> str:
    return Fernet.generate_key().decode()


def _get_fernet(settings: dict) -> tuple[Fernet | None, str]:
    key = settings.get("key", "").strip()
    if not key:
        key = Fernet.generate_key().decode()
        settings["_auto_key"] = key
    try:
        return Fernet(key.encode()), key
    except Exception as e:
        return None, str(e)


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        f, key_used = _get_fernet(settings)
        if f is None:
            return {"error": f"Key error: {key_used}"}
        token = f.encrypt(plaintext.encode("utf-8"))
        return {
            "output": token.decode(),
            "key_used": key_used,
            "info": f"Key used: {key_used}  (save to decrypt)",
        }
    except Exception as e:
        return {"error": f"Fernet encrypt failed: {e}"}


def decrypt(token: str, settings: dict) -> dict:
    try:
        f, _ = _get_fernet(settings)
        if f is None:
            return {"error": "Invalid key."}
        plaintext = f.decrypt(token.strip().encode())
        return {"output": plaintext.decode("utf-8")}
    except InvalidToken:
        return {"error": "Decryption failed: invalid token or wrong key."}
    except Exception as e:
        return {"error": f"Fernet decrypt failed: {e}"}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = encrypt(plaintext, settings)
    if "error" in result:
        return []
    return [
        ("Plaintext", plaintext),
        ("UTF-8 bytes", plaintext.encode("utf-8").hex()),
        ("AES-128-CBC Encrypt", "[encrypted bytes]"),
        ("HMAC-SHA256 Auth Tag", "[integrity tag appended]"),
        ("Fernet Token (Base64)", result["output"]),
    ]

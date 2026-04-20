"""
HMAC (Hash-based Message Authentication Code) using Python stdlib.
"""

import hmac
import hashlib
import base64

ID = "hmac"
NAME = "HMAC"
CATEGORY = "Authentication"
DESCRIPTION = "Keyed-hash message authentication code. Verifies both data integrity and message authenticity."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["authentication", "integrity", "keyed-hash"]

ALGORITHMS = ["SHA-256", "SHA-512", "SHA3-256", "SHA-1 (weak)", "MD5 (weak)"]

_ALGO_MAP = {
    "SHA-256":     "sha256",
    "SHA-512":     "sha512",
    "SHA3-256":    "sha3_256",
    "SHA-1 (weak)": "sha1",
    "MD5 (weak)":  "md5",
}


def default_settings() -> dict:
    return {"algorithm": "SHA-256", "key": "secret-key"}


def validate_settings(settings: dict) -> tuple[bool, str]:
    key = settings.get("key", "").strip()
    if not key:
        return False, "HMAC requires a secret key."
    return True, ""


def compute_hmac(message: str, settings: dict) -> dict:
    try:
        algo_name = settings.get("algorithm", "SHA-256")
        key = settings.get("key", "secret").strip()
        algo = _ALGO_MAP.get(algo_name, "sha256")

        h = hmac.new(key.encode("utf-8"), message.encode("utf-8"), algo)
        result_hex = h.hexdigest()
        result_b64 = base64.b64encode(h.digest()).decode()

        return {
            "output": result_hex,
            "base64": result_b64,
            "algorithm": algo_name,
        }
    except Exception as e:
        return {"error": f"HMAC failed: {e}"}


def verify_hmac(message: str, expected_mac: str, settings: dict) -> dict:
    try:
        result = compute_hmac(message, settings)
        if "error" in result:
            return result
        actual = result["output"]
        match = hmac.compare_digest(actual, expected_mac.strip().lower())
        return {"output": "VALID - MAC matches" if match else "INVALID - MAC does not match", "valid": match}
    except Exception as e:
        return {"error": f"HMAC verify failed: {e}"}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = compute_hmac(plaintext, settings)
    if "error" in result:
        return []
    return [
        ("Message", plaintext),
        ("Secret Key", settings.get("key", "")[:20] + ("..." if len(settings.get("key", "")) > 20 else "")),
        ("HMAC = H(key XOR opad || H(key XOR ipad || msg))", "[inner + outer hash]"),
        ("MAC Output (hex)", result["output"]),
    ]

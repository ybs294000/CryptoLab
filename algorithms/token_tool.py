"""
Secure random token generation using Python secrets stdlib.
"""

import secrets
import base64
import string

ID = "token"
NAME = "Secure Token Generator"
CATEGORY = "Randomness"
DESCRIPTION = "Cryptographically secure random token generation using Python secrets module."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = False
SUPPORTS_BATCH_MODE = False
TAGS = ["random", "token", "key generation", "secrets"]

TOKEN_TYPES = {
    "Hex Token":         "hex",
    "URL-Safe Base64":   "urlsafe",
    "Random Bytes (b64)": "bytes",
    "PIN (numeric)":     "pin",
    "Passphrase":        "passphrase",
    "API Key":           "apikey",
}

WORDLIST = [
    "alpha", "bravo", "cipher", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
    "xray", "yankee", "zulu", "aurora", "beacon", "castle", "drift", "ember",
    "frost", "glacier", "harbor", "island", "jungle", "knight", "lantern",
    "marble", "nebula", "orbit", "prism", "quartz", "raven", "silver", "tower",
]


def default_settings() -> dict:
    return {
        "token_type": "Hex Token",
        "length": 32,
        "count": 1,
    }


def validate_settings(settings: dict) -> tuple[bool, str]:
    length = settings.get("length", 32)
    if not isinstance(length, int) or length < 4 or length > 256:
        return False, "Length must be between 4 and 256."
    return True, ""


def generate(_, settings: dict) -> dict:
    try:
        token_type = TOKEN_TYPES.get(settings.get("token_type", "Hex Token"), "hex")
        length = int(settings.get("length", 32))
        count = int(settings.get("count", 1))
        count = min(count, 20)

        tokens = []
        for _ in range(count):
            if token_type == "hex":
                tokens.append(secrets.token_hex(length // 2))
            elif token_type == "urlsafe":
                tokens.append(secrets.token_urlsafe(length))
            elif token_type == "bytes":
                tokens.append(base64.b64encode(secrets.token_bytes(length)).decode())
            elif token_type == "pin":
                tokens.append("".join(secrets.choice(string.digits) for _ in range(length)))
            elif token_type == "passphrase":
                word_count = max(3, length // 6)
                words = [secrets.choice(WORDLIST) for _ in range(word_count)]
                tokens.append("-".join(words))
            elif token_type == "apikey":
                prefix = "clk"
                body = secrets.token_urlsafe(length)
                tokens.append(f"{prefix}_{body}")

        output = "\n".join(tokens)
        return {
            "output": output,
            "info": f"Generated {count} token(s) using cryptographically secure randomness (secrets module).",
        }
    except Exception as e:
        return {"error": f"Token generation failed: {e}"}

"""
Encoding utilities: Base64, Base32, Hex, URL, Binary.
All via Python stdlib - not encryption, just encoding.
"""

import base64
import binascii
import urllib.parse

ID = "encoding"
NAME = "Encoding Utilities"
CATEGORY = "Encoding"
DESCRIPTION = "Text/binary encoding schemes. Not encryption - easily reversible. Used for data transport."
STRENGTH = "none"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["encoding", "base64", "hex", "url", "binary"]

ALGORITHMS = {
    "Base64 Encode":   "base64_enc",
    "Base64 Decode":   "base64_dec",
    "Base32 Encode":   "base32_enc",
    "Base32 Decode":   "base32_dec",
    "Hex Encode":      "hex_enc",
    "Hex Decode":      "hex_dec",
    "URL Encode":      "url_enc",
    "URL Decode":      "url_dec",
    "Binary Encode":   "bin_enc",
    "Binary Decode":   "bin_dec",
    "ROT13":           "rot13",
}


def default_settings() -> dict:
    return {"algorithm": "Base64 Encode"}


def validate_settings(settings: dict) -> tuple[bool, str]:
    algo = settings.get("algorithm", "")
    if algo not in ALGORITHMS:
        return False, f"Unknown encoding: {algo}"
    return True, ""


def encode(text: str, settings: dict) -> dict:
    algo = settings.get("algorithm", "Base64 Encode")
    key = ALGORITHMS.get(algo)
    if not key:
        return {"error": f"Unknown algorithm: {algo}"}
    try:
        if key == "base64_enc":
            result = base64.b64encode(text.encode("utf-8")).decode()
        elif key == "base64_dec":
            result = base64.b64decode(text.strip().encode()).decode("utf-8", errors="replace")
        elif key == "base32_enc":
            result = base64.b32encode(text.encode("utf-8")).decode()
        elif key == "base32_dec":
            padded = text.strip().upper()
            missing = len(padded) % 8
            if missing:
                padded += "=" * (8 - missing)
            result = base64.b32decode(padded).decode("utf-8", errors="replace")
        elif key == "hex_enc":
            result = binascii.hexlify(text.encode("utf-8")).decode()
        elif key == "hex_dec":
            result = binascii.unhexlify(text.strip().replace(" ", "")).decode("utf-8", errors="replace")
        elif key == "url_enc":
            result = urllib.parse.quote(text, safe="")
        elif key == "url_dec":
            result = urllib.parse.unquote(text)
        elif key == "bin_enc":
            result = " ".join(format(b, "08b") for b in text.encode("utf-8"))
        elif key == "bin_dec":
            bits = text.strip().replace("\n", " ").split()
            result = "".join(chr(int(b, 2)) for b in bits if len(b) == 8)
        elif key == "rot13":
            import codecs
            result = codecs.encode(text, "rot_13")
        else:
            return {"error": "Unimplemented."}
        return {"output": result}
    except Exception as e:
        return {"error": f"Encoding failed: {e}"}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = encode(plaintext, settings)
    if "error" in result:
        return []
    algo = settings.get("algorithm", "Base64 Encode")
    return [
        ("Input", plaintext),
        (algo, result["output"]),
    ]

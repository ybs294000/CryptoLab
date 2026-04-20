"""
Hashing algorithms via Python hashlib stdlib.
Covers MD5, SHA-1, SHA-2 family, SHA-3 family, BLAKE2.
"""

import hashlib

ID = "hash"
NAME = "Hash Functions"
CATEGORY = "Hashing"
DESCRIPTION = "One-way cryptographic hash functions. Input -> fixed-size digest. Cannot be reversed."
STRENGTH = "varies"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["hash", "one-way", "digest", "integrity"]

ALGORITHMS = {
    "MD5":       {"func": "md5",       "strength": "weak",   "bits": 128, "note": "Broken - collision attacks known"},
    "SHA-1":     {"func": "sha1",      "strength": "weak",   "bits": 160, "note": "Deprecated - SHAttered collision attack"},
    "SHA-224":   {"func": "sha224",    "strength": "secure", "bits": 224, "note": "Part of SHA-2 family"},
    "SHA-256":   {"func": "sha256",    "strength": "secure", "bits": 256, "note": "Most widely used secure hash"},
    "SHA-384":   {"func": "sha384",    "strength": "secure", "bits": 384, "note": "Part of SHA-2 family"},
    "SHA-512":   {"func": "sha512",    "strength": "secure", "bits": 512, "note": "High security SHA-2"},
    "SHA3-224":  {"func": "sha3_224",  "strength": "secure", "bits": 224, "note": "Keccak-based, quantum resistant"},
    "SHA3-256":  {"func": "sha3_256",  "strength": "secure", "bits": 256, "note": "Keccak-based, quantum resistant"},
    "SHA3-384":  {"func": "sha3_384",  "strength": "secure", "bits": 384, "note": "Keccak-based, quantum resistant"},
    "SHA3-512":  {"func": "sha3_512",  "strength": "secure", "bits": 512, "note": "Keccak-based, quantum resistant"},
    "BLAKE2b":   {"func": "blake2b",   "strength": "secure", "bits": 512, "note": "Fast, secure. Used in Argon2"},
    "BLAKE2s":   {"func": "blake2s",   "strength": "secure", "bits": 256, "note": "Optimized for 32-bit platforms"},
}


def default_settings() -> dict:
    return {"algorithm": "SHA-256", "encoding": "hex"}


def validate_settings(settings: dict) -> tuple[bool, str]:
    algo = settings.get("algorithm", "SHA-256")
    if algo not in ALGORITHMS:
        return False, f"Unknown algorithm: {algo}"
    return True, ""


def hash_text(plaintext: str, settings: dict) -> dict:
    try:
        algo = settings.get("algorithm", "SHA-256")
        encoding = settings.get("encoding", "hex")
        func_name = ALGORITHMS[algo]["func"]

        h = hashlib.new(func_name)
        h.update(plaintext.encode("utf-8"))

        digest = h.digest()
        if encoding == "hex":
            result = h.hexdigest()
        elif encoding == "base64":
            import base64
            result = base64.b64encode(digest).decode()
        else:
            result = h.hexdigest()

        return {
            "output": result,
            "bits": ALGORITHMS[algo]["bits"],
            "bytes": len(digest),
            "note": ALGORITHMS[algo]["note"],
            "strength": ALGORITHMS[algo]["strength"],
        }
    except Exception as e:
        return {"error": f"Hash failed: {e}"}


def hash_all(plaintext: str) -> dict:
    """Compute all available hashes for comparison."""
    results = {}
    for algo in ALGORITHMS:
        r = hash_text(plaintext, {"algorithm": algo, "encoding": "hex"})
        results[algo] = r
    return results


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    result = hash_text(plaintext, settings)
    if "error" in result:
        return []
    algo = settings.get("algorithm", "SHA-256")
    return [
        ("Input Text", plaintext),
        ("UTF-8 Bytes", f"{len(plaintext.encode())} bytes"),
        (f"{algo} Hash Function", "[one-way transformation]"),
        (f"Digest ({result.get('bits', '')} bits)", result["output"]),
    ]

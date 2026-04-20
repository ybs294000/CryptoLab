"""
RSA asymmetric encryption using PyCryptodome.
Supports PKCS1-OAEP with SHA-256.
"""

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

ID = "rsa"
NAME = "RSA"
CATEGORY = "Modern Encryption"
DESCRIPTION = "Asymmetric public-key encryption. Encrypt with public key, decrypt with private key."
STRENGTH = "secure"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = False
TAGS = ["asymmetric", "public-key", "modern"]

KEY_SIZES = [1024, 2048, 4096]


def default_settings() -> dict:
    return {
        "key_size": 2048,
        "public_key": "",
        "private_key": "",
    }


def validate_settings(settings: dict) -> tuple[bool, str]:
    return True, ""


def generate_keypair(key_size: int = 2048) -> dict:
    try:
        key = RSA.generate(key_size)
        private_pem = key.export_key().decode()
        public_pem = key.publickey().export_key().decode()
        return {"public_key": public_pem, "private_key": private_pem}
    except Exception as e:
        return {"error": str(e)}


def encrypt(plaintext: str, settings: dict) -> dict:
    try:
        pub_key_pem = settings.get("public_key", "").strip()
        if not pub_key_pem:
            # Auto-generate for demo
            kp = generate_keypair(2048)
            if "error" in kp:
                return kp
            pub_key_pem = kp["public_key"]
            settings["_auto_private"] = kp["private_key"]
            settings["_auto_public"] = kp["public_key"]

        pub_key = RSA.import_key(pub_key_pem)
        cipher = PKCS1_OAEP.new(pub_key, hashAlgo=SHA256)
        data = plaintext.encode("utf-8")
        # RSA-OAEP max plaintext size depends on key size
        max_bytes = (pub_key.size_in_bytes()) - 2 * SHA256.digest_size - 2
        if len(data) > max_bytes:
            return {"error": f"Plaintext too long for RSA key ({len(data)} bytes, max {max_bytes})."}
        ciphertext = cipher.encrypt(data)
        return {
            "output": base64.b64encode(ciphertext).decode(),
            "info": "Encrypted with RSA-OAEP/SHA-256. Use private key to decrypt.",
        }
    except Exception as e:
        return {"error": f"RSA encrypt failed: {e}"}


def decrypt(ciphertext_b64: str, settings: dict) -> dict:
    try:
        priv_key_pem = settings.get("private_key", "").strip()
        if not priv_key_pem:
            priv_key_pem = settings.get("_auto_private", "")
        if not priv_key_pem:
            return {"error": "Private key required for RSA decryption."}
        priv_key = RSA.import_key(priv_key_pem)
        cipher = PKCS1_OAEP.new(priv_key, hashAlgo=SHA256)
        ciphertext = base64.b64decode(ciphertext_b64.strip())
        plaintext = cipher.decrypt(ciphertext)
        return {"output": plaintext.decode("utf-8")}
    except Exception as e:
        return {"error": f"RSA decrypt failed: {e}"}


def get_visualization_steps(plaintext: str, settings: dict) -> list:
    return [
        ("Plaintext", plaintext),
        ("RSA Public Key", "-----BEGIN PUBLIC KEY-----\n[key bytes]\n-----END PUBLIC KEY-----"),
        ("OAEP Padding + SHA-256", "[padded message block]"),
        ("RSA-OAEP Ciphertext", "[modular exponentiation result]"),
        ("Base64 Encoded Output", "[base64 ciphertext]"),
    ]

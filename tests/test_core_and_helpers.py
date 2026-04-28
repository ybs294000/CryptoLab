from __future__ import annotations

import unittest

from algorithms import encoding_tool
from core.registry import get_all, get_by_id, get_by_name
from utils.branding import LOGO_PATH, get_logo_base64
from utils.file_ops import build_secure_file_package, parse_secure_file_package
from utils.validators import validate_file_upload, validate_text_input

from tests.generate_sample_files import ensure_sample_files


class FakeUpload:
    def __init__(self, size: int) -> None:
        self.size = size


class CoreAndHelpersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = ensure_sample_files()

    def test_registry_contains_expected_algorithms(self) -> None:
        all_algorithms = get_all()
        self.assertGreaterEqual(len(all_algorithms), 10)
        self.assertIsNotNone(get_by_id("aes"))
        self.assertIsNotNone(get_by_name("AES"))
        self.assertIsNotNone(get_by_id("fernet"))
        self.assertIsNotNone(get_by_id("chacha20"))

    def test_logo_asset_available_for_branding(self) -> None:
        self.assertTrue(LOGO_PATH.exists())
        self.assertTrue(len(get_logo_base64()) > 100)

    def test_secure_package_roundtrip_metadata(self) -> None:
        package_bytes = build_secure_file_package(
            algorithm_id="aes",
            algorithm_settings={"mode": "GCM", "key_size": "AES-256"},
            original_name="sample_document.pdf",
            media_type="application/pdf",
            encrypted_output="ciphertext-placeholder",
        )
        ok, payload = parse_secure_file_package(package_bytes)
        self.assertTrue(ok)
        self.assertEqual(payload["algorithm_id"], "aes")
        self.assertEqual(payload["algorithm_settings"]["mode"], "GCM")
        self.assertEqual(payload["original_name"], "sample_document.pdf")

    def test_validate_text_input_limits(self) -> None:
        ok, _ = validate_text_input("hello")
        self.assertTrue(ok)
        ok, msg = validate_text_input("")
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_validate_file_upload_limits(self) -> None:
        ok, _ = validate_file_upload(FakeUpload(size=1024))
        self.assertTrue(ok)
        ok, msg = validate_file_upload(FakeUpload(size=0))
        self.assertFalse(ok)
        self.assertIn("empty", msg.lower())

    def test_uuencode_roundtrip_for_text(self) -> None:
        plaintext = "CryptoLab uuencode sample"
        encoded = encoding_tool.encode(plaintext, {"algorithm": "UU Encode"})
        self.assertNotIn("error", encoded)
        self.assertIn("begin 666 cryptolab.txt", encoded["output"])

        decoded = encoding_tool.encode(encoded["output"], {"algorithm": "UU Decode"})
        self.assertNotIn("error", decoded)
        self.assertEqual(plaintext, decoded["output"])


if __name__ == "__main__":
    unittest.main()

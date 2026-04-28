from __future__ import annotations

import unittest

import algorithms.aes_tool as aes_tool
import algorithms.chacha20_tool as chacha20_tool
from core.registry import get_by_id
from utils.file_ops import build_secure_file_package, parse_secure_file_package

from tests.generate_sample_files import ensure_sample_files


class SecureFileAlgorithmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = ensure_sample_files()
        cls.sample_payloads = {
            "png": cls.fixtures["logo"].read_bytes(),
            "pdf": cls.fixtures["pdf"].read_bytes(),
            "xlsx": cls.fixtures["xlsx"].read_bytes(),
            "bin": cls.fixtures["bin"].read_bytes(),
        }

    def _roundtrip(self, algo_id: str, settings: dict, payload_name: str) -> None:
        algo_entry = get_by_id(algo_id)
        self.assertIsNotNone(algo_entry, f"Algorithm {algo_id} must exist in registry")
        module = algo_entry["module"]
        raw_bytes = self.sample_payloads[payload_name]

        encrypted = module.encrypt_bytes(raw_bytes, dict(settings))
        self.assertNotIn("error", encrypted)
        self.assertIn("output", encrypted)

        package = build_secure_file_package(
            algorithm_id=algo_id,
            algorithm_settings=encrypted.get("package_settings", {}),
            original_name=f"fixture.{payload_name}",
            media_type="application/octet-stream",
            encrypted_output=encrypted["output"],
        )
        ok, parsed = parse_secure_file_package(package)
        self.assertTrue(ok)

        decrypt_settings = dict(settings)
        if encrypted.get("key_used"):
            decrypt_settings["key"] = encrypted["key_used"]
        decrypt_settings.update(parsed.get("algorithm_settings", {}))

        decrypted = module.decrypt_bytes(parsed["encrypted_output"], decrypt_settings)
        self.assertNotIn("error", decrypted)
        self.assertEqual(raw_bytes, decrypted["output_bytes"])

    def test_aes_gcm_roundtrip_for_binary_and_documents(self) -> None:
        settings = {"mode": "GCM", "key_size": "AES-256", "key": ""}
        for payload_name in ("png", "pdf", "xlsx", "bin"):
            with self.subTest(payload=payload_name):
                self._roundtrip("aes", settings, payload_name)

    def test_chacha20_roundtrip_for_binary_and_documents(self) -> None:
        settings = {"key": ""}
        for payload_name in ("png", "pdf", "xlsx", "bin"):
            with self.subTest(payload=payload_name):
                self._roundtrip("chacha20", settings, payload_name)

    def test_fernet_roundtrip_for_binary_and_documents(self) -> None:
        settings = {"key": ""}
        for payload_name in ("png", "pdf", "xlsx", "bin"):
            with self.subTest(payload=payload_name):
                self._roundtrip("fernet", settings, payload_name)

    def test_text_api_still_roundtrips_after_binary_support_added(self) -> None:
        cases = [
            ("aes", {"mode": "GCM", "key_size": "AES-256", "key": ""}),
            ("chacha20", {"key": ""}),
            ("fernet", {"key": ""}),
        ]
        plaintext = "CryptoLab roundtrip text"

        for algo_id, settings in cases:
            with self.subTest(algorithm=algo_id):
                module = get_by_id(algo_id)["module"]
                encrypted = module.encrypt(plaintext, dict(settings))
                self.assertNotIn("error", encrypted)
                decrypt_settings = dict(settings)
                if encrypted.get("key_used"):
                    decrypt_settings["key"] = encrypted["key_used"]
                decrypted = module.decrypt(encrypted["output"], decrypt_settings)
                self.assertEqual(plaintext, decrypted["output"])

    def test_aes_validation_accepts_exported_base64_key(self) -> None:
        encrypted = aes_tool.encrypt("CryptoLab AES", {"mode": "GCM", "key_size": "AES-256", "key": ""})
        self.assertNotIn("error", encrypted)
        ok, msg = aes_tool.validate_settings({"mode": "GCM", "key_size": "AES-256", "key": encrypted["key_used"]})
        self.assertTrue(ok, msg)

    def test_chacha_validation_accepts_exported_base64_key(self) -> None:
        encrypted = chacha20_tool.encrypt("CryptoLab ChaCha20", {"key": ""})
        self.assertNotIn("error", encrypted)
        ok, msg = chacha20_tool.validate_settings({"key": encrypted["key_used"]})
        self.assertTrue(ok, msg)


if __name__ == "__main__":
    unittest.main()

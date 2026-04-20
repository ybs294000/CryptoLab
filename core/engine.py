"""
CryptoLab engine - dispatches operations to algorithm modules.
"""

from core.registry import get_by_id, get_by_name
import time


def run_operation(algo_entry: dict, operation: str, text: str, settings: dict) -> dict:
    """
    Run an operation on an algorithm module.
    operation: encrypt | decrypt | hash | mac | encode | generate
    Returns dict with 'output' or 'error', plus optional metadata.
    """
    if algo_entry is None:
        return {"error": "Algorithm not found."}

    mod = algo_entry["module"]
    start = time.perf_counter()

    try:
        result = {}

        if operation == "encrypt":
            if hasattr(mod, "encrypt"):
                result = mod.encrypt(text, settings)
            else:
                result = {"error": f"{algo_entry['name']} does not support encryption."}

        elif operation == "decrypt":
            if hasattr(mod, "decrypt"):
                result = mod.decrypt(text, settings)
            else:
                result = {"error": f"{algo_entry['name']} does not support decryption."}

        elif operation == "hash":
            if hasattr(mod, "hash_text"):
                result = mod.hash_text(text, settings)
            else:
                result = {"error": f"{algo_entry['name']} does not support hashing."}

        elif operation == "mac":
            if hasattr(mod, "compute_hmac"):
                result = mod.compute_hmac(text, settings)
            elif hasattr(mod, "verify_hmac"):
                result = mod.verify_hmac(text, settings.get("expected_mac", ""), settings)
            else:
                result = {"error": "MAC not supported."}

        elif operation == "encode":
            if hasattr(mod, "encode"):
                result = mod.encode(text, settings)
            else:
                result = {"error": f"{algo_entry['name']} does not support encoding."}

        elif operation == "generate":
            if hasattr(mod, "generate"):
                result = mod.generate(text, settings)
            else:
                result = {"error": f"{algo_entry['name']} does not support generation."}

        else:
            result = {"error": f"Unknown operation: {operation}"}

    except Exception as e:
        result = {"error": f"Unexpected error in {algo_entry['name']}: {e}"}

    elapsed = time.perf_counter() - start
    result["elapsed_ms"] = round(elapsed * 1000, 3)
    return result


def get_default_operation(algo_entry: dict) -> str:
    mod = algo_entry["module"]
    if hasattr(mod, "encrypt"):
        return "encrypt"
    if hasattr(mod, "hash_text"):
        return "hash"
    if hasattr(mod, "compute_hmac"):
        return "mac"
    if hasattr(mod, "encode"):
        return "encode"
    if hasattr(mod, "generate"):
        return "generate"
    return "encrypt"


def get_available_operations(algo_entry: dict) -> list[str]:
    mod = algo_entry["module"]
    ops = []
    if hasattr(mod, "encrypt"):
        ops.append("encrypt")
    if hasattr(mod, "decrypt"):
        ops.append("decrypt")
    if hasattr(mod, "hash_text"):
        ops.append("hash")
    if hasattr(mod, "compute_hmac"):
        ops.append("mac")
    if hasattr(mod, "verify_hmac"):
        ops.append("verify")
    if hasattr(mod, "encode"):
        ops.append("encode")
    if hasattr(mod, "generate"):
        ops.append("generate")
    return ops

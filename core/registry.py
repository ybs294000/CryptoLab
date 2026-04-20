"""
Algorithm registry - central catalog of all available algorithm modules.
Add or remove entries here to control which algorithms appear in the app.
"""

from typing import Any

# Registry entry structure:
# {
#   "id": str,
#   "name": str,
#   "category": str,
#   "description": str,
#   "strength": "secure" | "legacy" | "weak" | "none",
#   "module": module object,
#   "modes": list[str] | None,
#   "supports_batch": bool,
#   "supports_viz": bool,
#   "tags": list[str],
# }

_REGISTRY: list[dict] = []
_REGISTRY_BUILT = False


def _build_registry() -> None:
    global _REGISTRY, _REGISTRY_BUILT
    if _REGISTRY_BUILT:
        return

    imports = [
        ("algorithms.aes_tool",      "encrypt/decrypt"),
        ("algorithms.fernet_tool",   "encrypt/decrypt"),
        ("algorithms.rsa_tool",      "encrypt/decrypt"),
        ("algorithms.chacha20_tool", "encrypt/decrypt"),
        ("algorithms.blowfish_tool", "encrypt/decrypt"),
        ("algorithms.tripledes_tool","encrypt/decrypt"),
        ("algorithms.hash_tool",     "hash"),
        ("algorithms.hmac_tool",     "mac"),
        ("algorithms.encoding_tool", "encode"),
        ("algorithms.token_tool",    "generate"),
        ("algorithms.classical_tool","encrypt/decrypt"),
    ]

    for module_path, _ in imports:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            entry = {
                "id":             getattr(mod, "ID", module_path),
                "name":           getattr(mod, "NAME", module_path),
                "category":       getattr(mod, "CATEGORY", "Other"),
                "description":    getattr(mod, "DESCRIPTION", ""),
                "strength":       getattr(mod, "STRENGTH", "unknown"),
                "module":         mod,
                "modes":          getattr(mod, "MODES", None),
                "supports_batch": getattr(mod, "SUPPORTS_BATCH_MODE", False),
                "supports_viz":   getattr(mod, "SUPPORTS_VISUALIZATION", False),
                "tags":           getattr(mod, "TAGS", []),
            }
            _REGISTRY.append(entry)
        except ImportError as e:
            # Gracefully skip unavailable modules
            print(f"[CryptoLab] Skipping {module_path}: {e}")

    _REGISTRY_BUILT = True


def get_all() -> list[dict]:
    _build_registry()
    return _REGISTRY


def get_by_id(algo_id: str) -> dict | None:
    _build_registry()
    for entry in _REGISTRY:
        if entry["id"] == algo_id:
            return entry
    return None


def get_by_category() -> dict[str, list[dict]]:
    _build_registry()
    cats: dict[str, list] = {}
    for entry in _REGISTRY:
        cat = entry["category"]
        cats.setdefault(cat, []).append(entry)
    return cats


def get_categories() -> list[str]:
    return list(get_by_category().keys())


def get_names() -> list[str]:
    return [e["name"] for e in get_all()]


def get_by_name(name: str) -> dict | None:
    _build_registry()
    for entry in _REGISTRY:
        if entry["name"] == name:
            return entry
    return None


def search(query: str) -> list[dict]:
    _build_registry()
    q = query.lower()
    results = []
    for entry in _REGISTRY:
        if (q in entry["name"].lower()
                or q in entry["category"].lower()
                or q in entry["description"].lower()
                or any(q in t for t in entry["tags"])):
            results.append(entry)
    return results

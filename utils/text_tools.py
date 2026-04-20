"""
Text and byte utility helpers.
"""

import binascii


def to_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def from_bytes(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def bytes_to_hex(data: bytes) -> str:
    return binascii.hexlify(data).decode("ascii")


def hex_to_bytes(hex_str: str) -> bytes:
    return binascii.unhexlify(hex_str)


def truncate_display(s: str, max_len: int = 500) -> str:
    if len(s) > max_len:
        return s[:max_len] + f"... [{len(s) - max_len} more chars]"
    return s


def entropy_estimate(data: bytes) -> float:
    """Shannon entropy estimate (bits per byte)."""
    import math
    if not data:
        return 0.0
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    n = len(data)
    entropy = -sum((c / n) * math.log2(c / n) for c in freq.values())
    return round(entropy, 4)


def char_frequencies(text: str) -> dict:
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: -x[1]))

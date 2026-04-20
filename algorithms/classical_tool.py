"""
Classical / historical cipher collection.
All implementations via pycipher and secretpy libraries - no hand-rolled logic.

Ciphers included (library-verified):
  pycipher : Caesar, Vigenere, Atbash, Affine, ROT13, Beaufort,
             Autokey, Bifid, Railfence, Gronsfeld, SimpleSubstitution, Playfair
  secretpy  : Scytale, Keyword Substitution

Educational note: These are historical ciphers. None provide
meaningful security by modern standards. They are included purely
for learning how classical cryptography evolved.
"""

import re
import string

try:
    import pycipher as _pc
    _PYCIPHER = True
except ImportError:
    _PYCIPHER = False

try:
    import secretpy as _sp
    _SECRETPY = True
except ImportError:
    _SECRETPY = False

ID = "classical"
NAME = "Classical Ciphers"
CATEGORY = "Classical (Educational)"
DESCRIPTION = (
    "Historical ciphers: Caesar, Vigenere, Playfair, Affine, Beaufort, "
    "Bifid, Railfence, Scytale, and more. Educational only - no security."
)
STRENGTH = "historical"
SUPPORTS_VISUALIZATION = True
SUPPORTS_BATCH_MODE = True
TAGS = ["classical", "historical", "caesar", "vigenere", "substitution", "transposition", "educational"]

# ----------------------------------------------------------------
# Cipher catalogue - defines every exposed cipher
# ----------------------------------------------------------------
CIPHER_CATALOGUE = {
    # name : {category, library, description, key_type, key_help}
    "Caesar": {
        "cat": "Monoalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Shifts each letter by a fixed number of positions (key = 1-25). Julius Caesar used shift 3.",
        "key_type": "int",
        "key_help": "Integer 1-25 (default: 3)",
        "key_default": 3,
        "era": "Ancient Rome (~50 BC)",
    },
    "ROT13": {
        "cat": "Monoalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Caesar cipher with fixed shift of 13. Self-inverse: encrypting twice gives the original.",
        "key_type": "none",
        "key_help": "No key needed (fixed shift 13)",
        "era": "20th century (internet era)",
    },
    "Atbash": {
        "cat": "Monoalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Reverses the alphabet: A=Z, B=Y, etc. Originally a Hebrew cipher for the aleph-beth alphabet.",
        "key_type": "none",
        "key_help": "No key needed",
        "era": "Ancient Hebrew (~600 BC)",
    },
    "Affine": {
        "cat": "Monoalphabetic Substitution",
        "lib": "pycipher",
        "desc": "E(x) = (ax + b) mod 26. Generalizes Caesar. 'a' must be coprime with 26 (1,3,5,7,9,11,15,17,19,21,23,25).",
        "key_type": "affine",
        "key_help": "a (must be coprime to 26) and b (0-25)",
        "era": "16th century",
    },
    "Simple Substitution": {
        "cat": "Monoalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Each letter maps to a unique fixed letter via a 26-character key alphabet. 26! possible keys.",
        "key_type": "str26",
        "key_help": "26 unique letters, e.g. QWERTYUIOPASDFGHJKLZXCVBNM",
        "key_default": "QWERTYUIOPASDFGHJKLZXCVBNM",
        "era": "Classical antiquity",
    },
    "Keyword Substitution": {
        "cat": "Monoalphabetic Substitution",
        "lib": "secretpy",
        "desc": "Builds a substitution alphabet by writing a keyword first, then remaining letters. Easier to remember than random key.",
        "key_type": "word",
        "key_help": "A word or phrase, e.g. KEYWORD",
        "key_default": "KEYWORD",
        "era": "Medieval / Renaissance",
    },
    "Vigenere": {
        "cat": "Polyalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Repeating-key Caesar. Each letter is shifted by the corresponding key letter. Broken by Kasiski test (1863).",
        "key_type": "word",
        "key_help": "Alphabetic keyword, e.g. KEY",
        "key_default": "KEY",
        "era": "16th century (Giovan Battista Bellaso, 1553)",
    },
    "Beaufort": {
        "cat": "Polyalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Variant of Vigenere. E(x) = (key - plaintext) mod 26. Reciprocal: same operation for encrypt and decrypt.",
        "key_type": "word",
        "key_help": "Alphabetic keyword",
        "key_default": "KEY",
        "era": "19th century (Sir Francis Beaufort)",
    },
    "Autokey": {
        "cat": "Polyalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Vigenere variant where the key is extended with the plaintext itself. Stronger than Vigenere but still broken by Friedman test.",
        "key_type": "word",
        "key_help": "Short primer keyword, e.g. KEY",
        "key_default": "KEY",
        "era": "16th century (Blaise de Vigenere, 1586)",
    },
    "Gronsfeld": {
        "cat": "Polyalphabetic Substitution",
        "lib": "pycipher",
        "desc": "Vigenere variant using digits (0-9) as key instead of letters. Weaker than Vigenere (only 10 shift values).",
        "key_type": "digits",
        "key_help": "Digits only, e.g. 1234",
        "key_default": "1234",
        "era": "17th century (Count Gronsfeld)",
    },
    "Playfair": {
        "cat": "Polygraphic Substitution",
        "lib": "pycipher",
        "desc": "Encrypts digraphs (letter pairs) using a 5x5 keyword grid. I and J share a cell. Used by British in WW1/WW2.",
        "key_type": "word",
        "key_help": "Keyword to build 5x5 grid (J treated as I), e.g. KEYWORD",
        "key_default": "KEYWORD",
        "era": "1854 (Charles Wheatstone, popularised by Lord Playfair)",
        "note": "Input stripped to alpha only. J replaced with I. Duplicate letters separated with X.",
    },
    "Bifid": {
        "cat": "Polygraphic Substitution",
        "lib": "pycipher",
        "desc": "Combines Polybius square with transposition. Uses a 5x5 key grid and a period for fractionation.",
        "key_type": "word_period",
        "key_help": "Keyword + period (integer, e.g. 5)",
        "key_default": "KEYWORD",
        "period_default": 5,
        "era": "1901 (Felix Delastelle)",
    },
    "Railfence": {
        "cat": "Transposition",
        "lib": "pycipher",
        "desc": "Writes plaintext in a zigzag pattern across N rails, then reads off row by row. Pure transposition - no substitution.",
        "key_type": "int",
        "key_help": "Number of rails (integer >= 2)",
        "key_default": 3,
        "era": "Ancient / American Civil War",
    },
    "Scytale": {
        "cat": "Transposition",
        "lib": "secretpy",
        "desc": "Ancient Spartan cipher. Wrap a strip of leather around a rod of specific diameter; writing reads normally only on the correct rod.",
        "key_type": "int",
        "key_help": "Rod diameter (integer >= 2, e.g. 4)",
        "key_default": 4,
        "era": "Ancient Sparta (~700 BC)",
    },
}

# Affine 'a' values that are coprime with 26
VALID_AFFINE_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]


# ----------------------------------------------------------------
# Text normalisation helpers
# ----------------------------------------------------------------

def _to_upper_alpha(text: str, replace_j: bool = False) -> str:
    """Strip to uppercase letters only. Optionally replace J with I."""
    t = text.upper()
    if replace_j:
        t = t.replace("J", "I")
    return re.sub(r"[^A-Z]", "", t)


def _build_playfair_key(keyword: str) -> str:
    """Build a 25-char keyed alphabet for Playfair (I=J merged)."""
    keyword = keyword.upper().replace("J", "I")
    seen: list[str] = []
    for ch in keyword + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    return "".join(seen[:25])


def _restore_case_and_nonalpha(original: str, processed: str, replace_j: bool = False) -> str:
    """
    Re-insert spaces and non-alpha from original into processed output.
    Processed is uppercase alpha-only result; we align it with original alpha chars.
    Used so output preserves word spacing for readability.
    """
    orig_alpha = [c for c in original.upper() if c.isalpha()]
    if replace_j:
        orig_alpha = ["I" if c == "J" else c for c in orig_alpha]

    proc = list(processed.upper())
    if len(proc) < len(orig_alpha):
        # Some ciphers (Playfair) may change length - just return as-is
        return processed

    result = []
    proc_idx = 0
    for ch in original:
        if ch.isalpha():
            if proc_idx < len(proc):
                # Preserve original case
                out_ch = proc[proc_idx].upper() if ch.isupper() else proc[proc_idx].lower()
                result.append(out_ch)
                proc_idx += 1
        else:
            result.append(ch)
    # Append any extra chars (Playfair padding)
    while proc_idx < len(proc):
        result.append(proc[proc_idx])
        proc_idx += 1
    return "".join(result)


# ----------------------------------------------------------------
# Default settings
# ----------------------------------------------------------------

def default_settings() -> dict:
    return {
        "cipher": "Caesar",
        "int_key": 3,
        "word_key": "KEY",
        "str26_key": "QWERTYUIOPASDFGHJKLZXCVBNM",
        "digits_key": "1234",
        "affine_a": 5,
        "affine_b": 8,
        "period": 5,
    }


def validate_settings(settings: dict) -> tuple[bool, str]:
    cipher = settings.get("cipher", "Caesar")
    info = CIPHER_CATALOGUE.get(cipher)
    if not info:
        return False, f"Unknown cipher: {cipher}"

    key_type = info["key_type"]

    if key_type == "int":
        k = settings.get("int_key", 3)
        if not isinstance(k, int) or k < 1:
            return False, "Key must be a positive integer."
        if cipher == "Caesar" and not (1 <= k <= 25):
            return False, "Caesar shift must be 1-25."
        if cipher in ("Railfence", "Scytale") and k < 2:
            return False, "Key must be >= 2."

    elif key_type == "word":
        k = settings.get("word_key", "").strip().upper()
        if not k or not k.isalpha():
            return False, "Key must be alphabetic letters only."

    elif key_type == "str26":
        k = settings.get("str26_key", "").upper().strip()
        if len(k) != 26 or len(set(k)) != 26 or not k.isalpha():
            return False, "Key must be exactly 26 unique letters."

    elif key_type == "digits":
        k = settings.get("digits_key", "").strip()
        if not k or not k.isdigit():
            return False, "Key must be digits only (0-9)."

    elif key_type == "affine":
        a = settings.get("affine_a", 5)
        b = settings.get("affine_b", 8)
        if a not in VALID_AFFINE_A:
            return False, f"'a' must be coprime with 26. Valid values: {VALID_AFFINE_A}"
        if not (0 <= b <= 25):
            return False, "b must be 0-25."

    elif key_type == "word_period":
        k = settings.get("word_key", "").strip().upper()
        if not k or not k.isalpha():
            return False, "Keyword must be alphabetic."
        p = settings.get("period", 5)
        if not isinstance(p, int) or p < 2:
            return False, "Period must be an integer >= 2."

    return True, ""


# ----------------------------------------------------------------
# Core dispatch
# ----------------------------------------------------------------

def _run(plaintext: str, settings: dict, mode: str) -> dict:
    if not _PYCIPHER and not _SECRETPY:
        return {"error": "Neither pycipher nor secretpy is installed. Run: pip install pycipher secretpy"}

    cipher = settings.get("cipher", "Caesar")
    info = CIPHER_CATALOGUE.get(cipher)
    if not info:
        return {"error": f"Unknown cipher: {cipher}"}

    encipher = (mode == "encrypt")
    lib = info["lib"]
    key_type = info["key_type"]

    try:
        # ---- Normalise input ----
        needs_j_strip = cipher in ("Playfair", "Bifid")
        upper_only = _to_upper_alpha(plaintext, replace_j=needs_j_strip)

        if not upper_only:
            return {"error": "No alphabetic characters in input. Classical ciphers operate on letters only."}

        # ---- pycipher branch ----
        if lib == "pycipher":
            if not _PYCIPHER:
                return {"error": "pycipher not installed."}

            if cipher == "Caesar":
                k = int(settings.get("int_key", 3))
                obj = _pc.Caesar(key=k)

            elif cipher == "ROT13":
                obj = _pc.Rot13()

            elif cipher == "Atbash":
                obj = _pc.Atbash()

            elif cipher == "Affine":
                a = int(settings.get("affine_a", 5))
                b = int(settings.get("affine_b", 8))
                obj = _pc.Affine(a=a, b=b)

            elif cipher == "Simple Substitution":
                k = settings.get("str26_key", "QWERTYUIOPASDFGHJKLZXCVBNM").upper().strip()
                obj = _pc.SimpleSubstitution(key=k)

            elif cipher == "Vigenere":
                k = settings.get("word_key", "KEY").upper().strip()
                obj = _pc.Vigenere(key=k)

            elif cipher == "Beaufort":
                k = settings.get("word_key", "KEY").upper().strip()
                obj = _pc.Beaufort(key=k)

            elif cipher == "Autokey":
                k = settings.get("word_key", "KEY").upper().strip()
                obj = _pc.Autokey(key=k)

            elif cipher == "Gronsfeld":
                k = [int(d) for d in settings.get("digits_key", "1234")]
                obj = _pc.Gronsfeld(key=k)

            elif cipher == "Playfair":
                kw = settings.get("word_key", "KEYWORD").upper().strip()
                key_alpha = _build_playfair_key(kw)
                obj = _pc.Playfair(key=key_alpha)

            elif cipher == "Bifid":
                kw = settings.get("word_key", "KEYWORD").upper().strip()
                key_alpha = _build_playfair_key(kw)  # same 25-char grid
                period = int(settings.get("period", 5))
                obj = _pc.Bifid(key=key_alpha, period=period)

            elif cipher == "Railfence":
                k = int(settings.get("int_key", 3))
                obj = _pc.Railfence(key=k)

            else:
                return {"error": f"Cipher {cipher} not mapped."}

            raw_out = obj.encipher(upper_only) if encipher else obj.decipher(upper_only)
            output = _restore_case_and_nonalpha(plaintext, raw_out, replace_j=needs_j_strip)

        # ---- secretpy branch ----
        elif lib == "secretpy":
            if not _SECRETPY:
                return {"error": "secretpy not installed."}

            alph = _sp.alphabets.ENGLISH  # list of 26 lowercase letters

            if cipher == "Keyword Substitution":
                k = settings.get("word_key", "KEYWORD").lower().strip()
                obj = _sp.Keyword()
                if encipher:
                    raw_out = obj.encrypt(upper_only.lower(), k, alph)
                else:
                    raw_out = obj.decrypt(upper_only.lower(), k, alph)
                output = _restore_case_and_nonalpha(plaintext, "".join(raw_out).upper())

            elif cipher == "Scytale":
                k = int(settings.get("int_key", 4))
                obj = _sp.Scytale()
                if encipher:
                    raw_out = obj.encrypt(upper_only.lower(), k, alph)
                else:
                    raw_out = obj.decrypt(upper_only.lower(), k, alph)
                output = _restore_case_and_nonalpha(plaintext, "".join(raw_out).upper())

            else:
                return {"error": f"Cipher {cipher} not mapped in secretpy branch."}

        else:
            return {"error": "Unknown library."}

        note = info.get("note", "")
        return {
            "output": output,
            "note": note if note else "",
            "info": f"{cipher} ({info['era']}) - {info['cat']}",
        }

    except Exception as e:
        return {"error": f"{cipher} failed: {e}"}


def encrypt(plaintext: str, settings: dict) -> dict:
    return _run(plaintext, settings, "encrypt")


def decrypt(ciphertext: str, settings: dict) -> dict:
    return _run(ciphertext, settings, "decrypt")


# ----------------------------------------------------------------
# Visualization
# ----------------------------------------------------------------

def get_visualization_steps(plaintext: str, settings: dict) -> list:
    cipher = settings.get("cipher", "Caesar")
    info = CIPHER_CATALOGUE.get(cipher, {})
    result = encrypt(plaintext, settings)
    if "error" in result:
        return []

    upper_in = _to_upper_alpha(plaintext)
    steps = [
        ("Original Input", plaintext),
        ("Alpha-only (uppercase)", upper_in),
        (f"{cipher} Cipher Applied", result["output"].upper()),
        ("Output (case restored)", result["output"]),
    ]

    # Caesar: show shift table for first 5 unique chars
    if cipher == "Caesar" and upper_in:
        shift = int(settings.get("int_key", 3))
        sample = []
        for ch in upper_in[:8]:
            enc_ch = chr((ord(ch) - 65 + shift) % 26 + 65)
            sample.append(f"{ch}->{enc_ch}")
        steps.insert(2, ("Shift Examples", "  ".join(sample)))

    # Vigenere/Beaufort/Autokey: show key extension
    if cipher in ("Vigenere", "Beaufort", "Autokey"):
        k = settings.get("word_key", "KEY").upper()
        extended = (k * (len(upper_in) // len(k) + 1))[:len(upper_in)]
        steps.insert(2, ("Key (extended)", extended[:40] + ("..." if len(extended) > 40 else "")))

    return steps

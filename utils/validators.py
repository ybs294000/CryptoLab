"""
Input validation helpers.
"""

MAX_INPUT_BYTES = 512 * 1024  # 512 KB


def validate_text_input(text: str) -> tuple[bool, str]:
    if not text or not text.strip():
        return False, "Input is empty."
    if len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        return False, f"Input too large (max {MAX_INPUT_BYTES // 1024} KB)."
    return True, ""


def validate_key(key: str, required_len: int | None = None) -> tuple[bool, str]:
    if not key or not key.strip():
        return False, "Key is empty."
    if required_len is not None and len(key) != required_len:
        return False, f"Key must be exactly {required_len} characters."
    return True, ""


def validate_file_upload(uploaded_file) -> tuple[bool, str]:
    if uploaded_file is None:
        return False, "No file uploaded."
    if uploaded_file.size == 0:
        return False, "Uploaded file is empty."
    if uploaded_file.size > MAX_INPUT_BYTES:
        return False, f"File too large (max {MAX_INPUT_BYTES // 1024} KB)."
    return True, ""

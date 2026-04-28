"""
Batch tab - text batch processing plus secure file protection.
"""

from __future__ import annotations

import streamlit as st

from core.registry import get_all, get_by_id, get_by_name
from core.engine import run_operation
from utils.branding import render_brand_header
from utils.file_ops import (
    build_secure_file_package,
    parse_secure_file_package,
    read_uploaded_bytes,
    read_uploaded_text,
)
from utils.ui_helpers import error_box, info_box, show_output_box, success_box
from utils.validators import validate_file_upload


SECURE_FILE_ALGOS = {
    "AES-GCM": {
        "id": "aes",
        "settings": {"mode": "GCM", "key_size": "AES-256", "key": ""},
        "description": "Widely used authenticated encryption for files and documents.",
    },
    "ChaCha20-Poly1305": {
        "id": "chacha20",
        "settings": {"key": ""},
        "description": "Fast authenticated encryption, especially strong on mobile and mixed hardware.",
    },
    "Fernet": {
        "id": "fernet",
        "settings": {"key": ""},
        "description": "Simple authenticated encryption with a ready-to-store application key.",
    },
}


def _text_batch_settings(algo_entry: dict) -> dict:
    settings = {}
    if hasattr(algo_entry["module"], "default_settings"):
        settings = algo_entry["module"].default_settings()

    if algo_entry["id"] in ("aes", "chacha20", "blowfish", "tripledes"):
        settings["key"] = st.text_input(
            "Key",
            type="password",
            key="batch_key",
            help="Leave blank to auto-generate a key for encryption workflows.",
        )
    elif algo_entry["id"] == "fernet":
        col_fk, col_fg = st.columns([3, 1])
        with col_fk:
            settings["key"] = st.text_input("Fernet Key", type="password", key="batch_fernet_key")
        with col_fg:
            if st.button(":material/key: Generate", key="batch_fernet_gen"):
                import algorithms.fernet_tool as ft

                st.session_state["batch_fernet_generated"] = ft.generate_key()
        if "batch_fernet_generated" in st.session_state:
            st.code(st.session_state["batch_fernet_generated"])
            st.caption("Save this key if you want to decrypt later.")
    elif algo_entry["id"] == "hmac":
        settings["key"] = st.text_input("HMAC Secret Key", value="secret-key", key="batch_hmac_key")
    elif algo_entry["id"] == "encoding":
        import algorithms.encoding_tool as et

        settings["algorithm"] = st.selectbox(
            "Encoding Type",
            list(et.ALGORITHMS.keys()),
            key="batch_enc_algo",
        )
    elif algo_entry["id"] == "hash":
        import algorithms.hash_tool as ht

        settings["algorithm"] = st.selectbox(
            "Hash Algorithm",
            list(ht.ALGORITHMS.keys()),
            index=3,
            key="batch_hash_algo",
        )
    return settings


def _clean_package_settings(settings: dict | None) -> dict:
    if not isinstance(settings, dict):
        return {}
    return {
        key: value
        for key, value in settings.items()
        if not str(key).startswith("_") and key != "key"
    }


def _file_vault_settings(label: str, algorithm_name: str, *, package_settings: dict | None = None, encrypting: bool = True) -> tuple[str, dict]:
    algo_config = SECURE_FILE_ALGOS[algorithm_name]
    clean_package_settings = _clean_package_settings(package_settings)
    settings = dict(algo_config["settings"])
    settings.update(clean_package_settings)
    algorithm_id = algo_config["id"]

    if algorithm_id == "aes":
        detected_aes_settings = bool(clean_package_settings)
        if encrypting or not detected_aes_settings:
            default_key_size = settings.get("key_size", "AES-256")
            settings["key_size"] = st.selectbox(
                "Key Strength",
                ["AES-128", "AES-192", "AES-256"],
                index=["AES-128", "AES-192", "AES-256"].index(default_key_size),
                key=f"{label}_aes_key_size",
                help="AES-256 is recommended for file protection.",
            )
            settings["mode"] = st.selectbox(
                "Mode",
                ["GCM", "EAX", "CBC"],
                index=["GCM", "EAX", "CBC"].index(settings.get("mode", "GCM")),
                key=f"{label}_aes_mode",
                help="GCM is recommended because it includes tamper detection.",
            )
        else:
            st.text_input(
                "Detected Key Strength",
                value=settings.get("key_size", "AES-256"),
                disabled=True,
                key=f"{label}_aes_key_size_detected",
            )
            st.text_input(
                "Detected Mode",
                value=settings.get("mode", "GCM"),
                disabled=True,
                key=f"{label}_aes_mode_detected",
            )
        settings["key"] = st.text_input(
            "Encryption Key",
            type="password",
            key=f"{label}_aes_key",
            help="Leave blank to auto-generate a key. For decryption, paste the base64 key shown after encryption or use an exact ASCII key of the required length.",
        )
    elif algorithm_id == "chacha20":
        settings["key"] = st.text_input(
            "Encryption Key",
            type="password",
            key=f"{label}_chacha_key",
            help="Leave blank to auto-generate a key. For decryption, paste the base64 key shown after encryption or use an exact 32-character ASCII key.",
        )
    elif algorithm_id == "fernet":
        col1, col2 = st.columns([3, 1])
        with col1:
            settings["key"] = st.text_input(
                "Fernet Key",
                type="password",
                key=f"{label}_fernet_key",
                help="Leave blank to auto-generate a Fernet key.",
            )
        with col2:
            if st.button(":material/key: Generate", key=f"{label}_fernet_generate"):
                import algorithms.fernet_tool as ft

                st.session_state[f"{label}_fernet_generated"] = ft.generate_key()
        generated = st.session_state.get(f"{label}_fernet_generated")
        if generated:
            settings["key"] = settings["key"] or generated
            st.code(generated)
            st.caption("Generated key ready to use for file encryption.")

    return algorithm_id, settings


def _clear_file_result_if_needed(signature: tuple) -> None:
    previous = st.session_state.get("batch_file_signature")
    if previous != signature:
        st.session_state.pop("batch_file_result", None)
        st.session_state["batch_file_signature"] = signature


def _render_text_batch() -> None:
    st.markdown("### :material/article: Text File Processing")
    st.caption("Process plain-text files with encryption, hashing, MAC, or encoding tools.")

    all_algos = [a for a in get_all() if a.get("supports_batch", False)]
    algo_names = [a["name"] for a in all_algos]

    col1, col2 = st.columns([2, 2])
    with col1:
        uploaded = st.file_uploader(
            "Upload a text file",
            type=["txt"],
            key="batch_upload",
        )
    with col2:
        selected_name = st.selectbox("Algorithm", algo_names, key="batch_algo")
        algo_entry = get_by_name(selected_name)

        operation = "encode"
        if algo_entry:
            ops = []
            mod = algo_entry["module"]
            if hasattr(mod, "encrypt"):
                ops.append("Encrypt")
            if hasattr(mod, "decrypt"):
                ops.append("Decrypt")
            if hasattr(mod, "hash_text"):
                ops.append("Hash")
            if hasattr(mod, "compute_hmac"):
                ops.append("MAC")
            if hasattr(mod, "encode"):
                ops.append("Encode")

            op_label = st.selectbox("Operation", ops if ops else ["N/A"], key="batch_op")
            op_map = {
                "Encrypt": "encrypt",
                "Decrypt": "decrypt",
                "Hash": "hash",
                "MAC": "mac",
                "Encode": "encode",
            }
            operation = op_map.get(op_label, "encode")

    if algo_entry is None:
        error_box("Algorithm not found.", title="Unavailable Algorithm")
        return

    settings = _text_batch_settings(algo_entry)
    run_batch = st.button(":material/play_arrow: Process Text File", type="primary", key="batch_run")

    if run_batch:
        ok, msg = validate_file_upload(uploaded)
        if not ok:
            error_box(msg, title="Upload Problem")
            return

        success, content, enc = read_uploaded_text(uploaded)
        if not success:
            error_box(content, title="Read Problem")
            return

        if hasattr(algo_entry["module"], "validate_settings"):
            valid, vmsg = algo_entry["module"].validate_settings(settings)
            if not valid:
                error_box(f"Settings error: {vmsg}", title="Settings Problem")
                return

        with st.spinner(f"Processing {uploaded.name}..."):
            result = run_operation(algo_entry, operation, content, settings)

        if "error" in result:
            error_box(result["error"], title="Processing Failed")
            return

        output = result.get("output", "")
        success_box(
            f"Processed {len(content)} characters in {result.get('elapsed_ms', 0)} ms.",
            title="Text File Processed",
        )
        show_output_box("Result Preview", output[:1200] if output else "")

        dl_col, info_col = st.columns([1, 2])
        with dl_col:
            file_name = f"cryptolab_{uploaded.name.replace('.txt', '')}_processed.txt"
            st.download_button(
                ":material/download: Download Result",
                data=output.encode("utf-8"),
                file_name=file_name,
                mime="text/plain",
                key=f"batch_download_{uploaded.name}_{operation}",
            )
        with info_col:
            st.caption(f"Detected encoding: {enc}")
            if result.get("key_used"):
                show_output_box("Key Used", result["key_used"])
            if result.get("info"):
                info_box(result["info"], title="Processing Details")


def _render_secure_file_vault() -> None:
    st.markdown("### :material/lock: Secure File Vault")
    st.caption(
        "Encrypt and decrypt images and documents such as PNG, JPG, PDF, XLSX, DOCX, CSV, and other common files using authenticated encryption."
    )

    operation = st.radio(
        "Workflow",
        ["Encrypt File", "Decrypt Secure Package"],
        horizontal=True,
        key="file_vault_operation",
    )

    encrypting = operation == "Encrypt File"
    allowed_help = "Upload any supported file. The encrypted result is exported as a `.cryptolab` secure package."
    decrypt_help = "Upload a `.cryptolab` package to restore the original file."
    uploaded = st.file_uploader(
        "Choose a file",
        type=None if encrypting else ["cryptolab"],
        key="file_vault_upload",
        help=allowed_help if encrypting else decrypt_help,
    )

    package_data = None
    if encrypting:
        selected_algorithm_name = st.selectbox(
            "Protection Algorithm",
            list(SECURE_FILE_ALGOS.keys()),
            key="file_vault_encrypt_algo",
        )
    else:
        selected_algorithm_name = "AES-GCM"

    if not encrypting and uploaded is not None:
        success, raw_or_error = read_uploaded_bytes(uploaded)
        if success:
            parsed_ok, payload_or_error = parse_secure_file_package(raw_or_error)
            if parsed_ok:
                package_data = payload_or_error
                algo_entry = get_by_id(package_data["algorithm_id"])
                if algo_entry is not None:
                    for display_name, config in SECURE_FILE_ALGOS.items():
                        if config["id"] == algo_entry["id"]:
                            selected_algorithm_name = display_name
                            break
                    info_box(
                        f"Detected package for {package_data.get('original_name', 'original file')} using {algo_entry['name']}.",
                        title="Package Detected",
                    )
                    if algo_entry["id"] == "aes" and not package_data.get("algorithm_settings"):
                        warning_message = (
                            "This package was created before CryptoLab started storing AES mode and key strength inside the package. "
                            "Select the original AES settings manually before decrypting."
                        )
                        info_box(warning_message, title="Older Package")
                else:
                    error_box("The package references an unsupported algorithm.", title="Unsupported Package")
            else:
                error_box(payload_or_error, title="Package Problem")

    if not encrypting:
        st.text_input(
            "Detected Algorithm",
            value=selected_algorithm_name,
            disabled=True,
            key="file_vault_detected_algo",
        )

    st.caption(SECURE_FILE_ALGOS[selected_algorithm_name]["description"])
    package_settings = package_data.get("algorithm_settings", {}) if package_data else {}
    algorithm_id, settings = _file_vault_settings(
        "file_vault",
        selected_algorithm_name,
        package_settings=package_settings,
        encrypting=encrypting,
    )
    algo_entry = get_by_id(algorithm_id)

    if algo_entry is None:
        error_box("The selected protection algorithm is not available.", title="Unavailable Algorithm")
        return

    file_name = uploaded.name if uploaded is not None else ""
    file_size = getattr(uploaded, "size", 0)
    signature = (operation, file_name, file_size, selected_algorithm_name)
    _clear_file_result_if_needed(signature)

    run_label = ":material/encrypted: Encrypt File" if encrypting else ":material/no_encryption: Decrypt Package"
    run_key = "file_vault_run_encrypt" if encrypting else "file_vault_run_decrypt"
    if st.button(run_label, type="primary", key=run_key):
        ok, msg = validate_file_upload(uploaded)
        if not ok:
            error_box(msg, title="Upload Problem")
            return

        if hasattr(algo_entry["module"], "validate_settings"):
            valid, vmsg = algo_entry["module"].validate_settings(settings)
            if not valid:
                error_box(f"Settings error: {vmsg}", title="Settings Problem")
                return

        success, raw_or_error = read_uploaded_bytes(uploaded)
        if not success:
            error_box(raw_or_error, title="Read Problem")
            return

        raw_bytes = raw_or_error

        if encrypting:
            if not hasattr(algo_entry["module"], "encrypt_bytes"):
                error_box("This algorithm does not support secure file encryption.", title="Unsupported Workflow")
                return

            with st.spinner(f"Encrypting {uploaded.name}..."):
                result = algo_entry["module"].encrypt_bytes(raw_bytes, settings)

            if "error" in result:
                error_box(result["error"], title="Encryption Failed")
                return

            package_bytes = build_secure_file_package(
                algorithm_id=algorithm_id,
                algorithm_settings=result.get("package_settings", _clean_package_settings(settings)),
                original_name=uploaded.name,
                media_type=uploaded.type or "application/octet-stream",
                encrypted_output=result["output"],
            )
            st.session_state["batch_file_result"] = {
                "mode": "encrypt",
                "package_name": f"{uploaded.name}.cryptolab",
                "package_bytes": package_bytes,
                "key_used": result.get("key_used", ""),
                "info": result.get("info", ""),
                "original_name": uploaded.name,
                "algorithm_name": selected_algorithm_name,
                "package_settings": result.get("package_settings", _clean_package_settings(settings)),
            }
        else:
            if package_data is None:
                error_box("Upload a valid `.cryptolab` file to decrypt.", title="Package Required")
                return
            if package_data.get("algorithm_id") != algorithm_id:
                algo_entry = get_by_id(package_data.get("algorithm_id", ""))
                if algo_entry is None:
                    error_box("The package uses an unsupported algorithm.", title="Unsupported Package")
                    return
            if not hasattr(algo_entry["module"], "decrypt_bytes"):
                error_box("This package cannot be decrypted with the current algorithm support.", title="Unsupported Workflow")
                return

            decrypt_settings = dict(settings)
            decrypt_settings.update(package_data.get("algorithm_settings", {}))

            with st.spinner(f"Decrypting {uploaded.name}..."):
                result = algo_entry["module"].decrypt_bytes(package_data["encrypted_output"], decrypt_settings)

            if "error" in result:
                error_box(result["error"], title="Decryption Failed")
                return

            restored_name = package_data.get("original_name", "restored_file")
            restored_type = package_data.get("media_type", "application/octet-stream")
            st.session_state["batch_file_result"] = {
                "mode": "decrypt",
                "restored_name": restored_name,
                "restored_type": restored_type,
                "restored_bytes": result["output_bytes"],
                "info": f"Decrypted with {algo_entry['name']}. Original file ready to download.",
                "algorithm_name": algo_entry["name"],
            }

    result = st.session_state.get("batch_file_result")
    if not result:
        return

    st.markdown("---")
    if result["mode"] == "encrypt":
        success_box(
            f"Protected `{result['original_name']}` with {result['algorithm_name']}. Download the secure package and keep the key in a safe place.",
            title="Secure Package Ready",
        )
        action_col, meta_col = st.columns([1, 2])
        with action_col:
            st.download_button(
                ":material/download: Download Secure Package",
                data=result["package_bytes"],
                file_name=result["package_name"],
                mime="application/octet-stream",
                key=f"file_vault_download_encrypt_{result['package_name']}",
            )
        with meta_col:
            if result.get("key_used"):
                show_output_box("Encryption Key", result["key_used"])
                info_box(
                    "This is the exact key to reuse during decryption. For AES and ChaCha20, CryptoLab shows the auto-generated key in base64 so it can be copied safely without losing bytes.",
                    title="Save This Key",
                )
            if result.get("info"):
                info_box(result["info"], title="Encryption Details")
    else:
        success_box(
            f"Restored `{result['restored_name']}` from the secure package. Review the file name before saving or sharing it.",
            title="Original File Restored",
        )
        action_col, meta_col = st.columns([1, 2])
        with action_col:
            st.download_button(
                ":material/download: Download Restored File",
                data=result["restored_bytes"],
                file_name=result["restored_name"],
                mime=result["restored_type"],
                key=f"file_vault_download_decrypt_{result['restored_name']}",
            )
        with meta_col:
            info_box(result["info"], title="Decryption Details")


def render() -> None:
    render_brand_header(
        "Batch Processing",
        "Work with text files in bulk or protect images and documents with authenticated encryption.",
        compact=True,
    )

    _render_text_batch()
    st.markdown("---")
    _render_secure_file_vault()

    st.markdown("---")
    info_box(
        "Maximum upload size is 512 KB in the current app configuration. Secure file protection is designed for binary files such as images and office documents. The encrypted output is a CryptoLab package, not the original file format, so it can be stored or transferred safely. If you let the app generate a key, save it immediately. Without that key, decryption is not possible later.",
        title="File Safety Notes",
    )

"""
Batch tab - upload a .txt file and process it with a chosen algorithm.
"""

import streamlit as st
from core.registry import get_all, get_by_name
from core.engine import run_operation, get_default_operation
from utils.validators import validate_file_upload
from utils.file_ops import read_uploaded_text


def render() -> None:
    st.markdown("### Batch File Processing")
    st.caption("Upload a .txt file and process its contents with any algorithm.")

    all_algos = [a for a in get_all() if a.get("supports_batch", False)]
    algo_names = [a["name"] for a in all_algos]

    col1, col2 = st.columns([2, 2])
    with col1:
        uploaded = st.file_uploader(
            "Upload .txt file",
            type=["txt"],
            key="batch_upload",
        )
    with col2:
        selected_name = st.selectbox("Algorithm", algo_names, key="batch_algo")
        algo_entry = get_by_name(selected_name)

        if algo_entry:
            ops = []
            mod = algo_entry["module"]
            if hasattr(mod, "encrypt"):    ops.append("Encrypt")
            if hasattr(mod, "decrypt"):    ops.append("Decrypt")
            if hasattr(mod, "hash_text"):  ops.append("Hash")
            if hasattr(mod, "compute_hmac"): ops.append("MAC")
            if hasattr(mod, "encode"):     ops.append("Encode")

            op_label = st.selectbox("Operation", ops if ops else ["N/A"], key="batch_op")
            op_map = {
                "Encrypt": "encrypt", "Decrypt": "decrypt",
                "Hash": "hash", "MAC": "mac", "Encode": "encode",
            }
            operation = op_map.get(op_label, "encode")

    # Quick settings for batch
    settings = {}
    if algo_entry:
        if hasattr(algo_entry["module"], "default_settings"):
            settings = algo_entry["module"].default_settings()

        # Minimal key override for encrypt modes
        if algo_entry["id"] in ("aes", "chacha20", "blowfish", "tripledes"):
            settings["key"] = st.text_input(
                "Key (leave blank to auto-generate)",
                type="password", key="batch_key"
            )
        elif algo_entry["id"] == "fernet":
            col_fk, col_fg = st.columns([3, 1])
            with col_fk:
                settings["key"] = st.text_input("Fernet Key", type="password", key="batch_fernet_key")
            with col_fg:
                if st.button("Generate", key="batch_fernet_gen"):
                    import algorithms.fernet_tool as ft
                    st.session_state["batch_fernet_generated"] = ft.generate_key()
            if "batch_fernet_generated" in st.session_state:
                st.code(st.session_state["batch_fernet_generated"])
        elif algo_entry["id"] == "hmac":
            settings["key"] = st.text_input("HMAC Secret Key", value="secret-key", key="batch_hmac_key")
        elif algo_entry["id"] == "encoding":
            import algorithms.encoding_tool as et
            settings["algorithm"] = st.selectbox("Encoding Type", list(et.ALGORITHMS.keys()), key="batch_enc_algo")
        elif algo_entry["id"] == "hash":
            import algorithms.hash_tool as ht
            settings["algorithm"] = st.selectbox("Hash Algorithm", list(ht.ALGORITHMS.keys()), index=3, key="batch_hash_algo")

    run_batch = st.button(":material/play_arrow: Process File", type="primary", key="batch_run")

    if run_batch:
        ok, msg = validate_file_upload(uploaded)
        if not ok:
            st.error(msg)
            return

        success, content, enc = read_uploaded_text(uploaded)
        if not success:
            st.error(content)
            return

        if algo_entry is None:
            st.error("Algorithm not found.")
            return

        # Validate settings
        if hasattr(algo_entry["module"], "validate_settings"):
            valid, vmsg = algo_entry["module"].validate_settings(settings)
            if not valid:
                st.error(f"Settings error: {vmsg}")
                return

        with st.spinner(f"Processing {uploaded.name}..."):
            result = run_operation(algo_entry, operation, content, settings)

        if "error" in result:
            st.error(result["error"])
        else:
            output = result.get("output", "")
            st.success(f"Processed {len(content)} chars in {result.get('elapsed_ms', 0)} ms")

            with st.expander("Preview (first 500 chars)"):
                st.code(output[:500])

            dl_col, info_col = st.columns([1, 2])
            with dl_col:
                fname = f"cryptolab_{uploaded.name.replace('.txt','')}_processed.txt"
                st.download_button(
                    ":material/download: Download Result",
                    data=output.encode("utf-8"),
                    file_name=fname,
                    mime="text/plain",
                    key="batch_download",
                )
            with info_col:
                if result.get("key_used"):
                    with st.expander("Key used (save to decrypt)"):
                        st.code(result["key_used"])
                if result.get("info"):
                    st.info(result["info"])

    # Info box
    st.markdown("---")
    st.markdown("""
<div style="background:#141A22;border:1px solid #283142;border-radius:8px;padding:14px 18px;">
  <b style="color:#4F8EF7;">Batch Mode Notes</b><br>
  <span style="color:#9CA6B5;font-size:13px;">
  Maximum file size: 512 KB. Only UTF-8 or Latin-1 text files supported.
  If using auto-generated keys (blank key field), save the key shown after processing to decrypt later.
  RSA is not available in batch mode due to plaintext size limitations.
  </span>
</div>
""", unsafe_allow_html=True)

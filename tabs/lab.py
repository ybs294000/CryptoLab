"""
Lab tab - main working area for algorithm operations.
"""

import streamlit as st
import time
from core.registry import get_all, get_by_category, get_by_name
from core.engine import run_operation, get_available_operations, get_default_operation
from utils.validators import validate_text_input
from utils.text_tools import entropy_estimate, char_frequencies
from utils.ui_helpers import pipeline_viz, error_box, success_box, warning_box


STRENGTH_COLOR = {
    "secure": "#22C55E",
    "legacy": "#F59E0B",
    "weak":   "#EF4444",
    "none":   "#4F8EF7",
    "varies": "#9CA6B5",
}

OP_LABELS = {
    "encrypt":  "Encrypt",
    "decrypt":  "Decrypt",
    "hash":     "Hash",
    "mac":      "Compute MAC",
    "verify":   "Verify MAC",
    "encode":   "Encode / Decode",
    "generate": "Generate",
}


def _get_settings_panel(algo_entry: dict, operation: str) -> dict:
    """Render dynamic settings panel for the selected algorithm."""
    mod = algo_entry["module"]
    settings = {}

    if not hasattr(mod, "default_settings"):
        return settings

    defaults = mod.default_settings()

    # --- AES ---
    if algo_entry["id"] == "aes":
        settings["key_size"] = st.selectbox(
            "Key Size", ["AES-128", "AES-192", "AES-256"],
            index=2, key="aes_key_size"
        )
        settings["mode"] = st.selectbox(
            "Mode", ["GCM", "EAX", "CBC"],
            key="aes_mode"
        )
        settings["key"] = st.text_input(
            "Key (leave blank to auto-generate)",
            type="password", key="aes_key",
            help="For AES-256: 32 chars. AES-128: 16 chars. AES-192: 24 chars."
        )

    # --- Fernet ---
    elif algo_entry["id"] == "fernet":
        col1, col2 = st.columns([3, 1])
        with col1:
            settings["key"] = st.text_input(
                "Fernet Key (leave blank to auto-generate)",
                type="password", key="fernet_key",
                help="Must be a valid Fernet key (URL-safe base64, 32 bytes)."
            )
        with col2:
            if st.button("Generate Key", key="fernet_gen_key"):
                import algorithms.fernet_tool as ft
                new_key = ft.generate_key()
                st.session_state["_fernet_generated"] = new_key
        if "_fernet_generated" in st.session_state:
            st.code(st.session_state["_fernet_generated"])
            st.caption("Copy this key - you need it to decrypt.")

    # --- RSA ---
    elif algo_entry["id"] == "rsa":
        settings["key_size"] = st.selectbox("Key Size", [2048, 4096, 1024], key="rsa_key_size")
        gen_col, _ = st.columns([1, 2])
        with gen_col:
            if st.button("Generate RSA Key Pair", key="rsa_gen"):
                import algorithms.rsa_tool as rt
                kp = rt.generate_keypair(settings["key_size"])
                if "error" not in kp:
                    st.session_state["rsa_public"] = kp["public_key"]
                    st.session_state["rsa_private"] = kp["private_key"]
                else:
                    error_box(kp["error"])

        if operation == "encrypt":
            settings["public_key"] = st.text_area(
                "Public Key (PEM) - leave blank to auto-generate",
                value=st.session_state.get("rsa_public", ""),
                height=80, key="rsa_pub_input"
            )
        else:
            settings["public_key"] = st.session_state.get("rsa_public", "")
            settings["private_key"] = st.text_area(
                "Private Key (PEM)",
                value=st.session_state.get("rsa_private", ""),
                height=80, key="rsa_priv_input"
            )

    # --- ChaCha20 ---
    elif algo_entry["id"] == "chacha20":
        settings["key"] = st.text_input(
            "Key (leave blank to auto-generate)",
            type="password", key="chacha_key",
            help="32 ASCII characters for a 256-bit key."
        )

    # --- Blowfish ---
    elif algo_entry["id"] == "blowfish":
        settings["key"] = st.text_input(
            "Key (4-56 chars, blank to auto-generate)",
            type="password", key="blowfish_key"
        )

    # --- Triple DES ---
    elif algo_entry["id"] == "tripledes":
        settings["key"] = st.text_input(
            "Key (blank to auto-generate)",
            type="password", key="des3_key"
        )

    # --- Hash ---
    elif algo_entry["id"] == "hash":
        algo_list = list(__import__("algorithms.hash_tool", fromlist=["ALGORITHMS"]).ALGORITHMS.keys())
        settings["algorithm"] = st.selectbox("Hash Algorithm", algo_list, index=3, key="hash_algo")
        settings["encoding"] = st.selectbox("Output Encoding", ["hex", "base64"], key="hash_enc")

    # --- HMAC ---
    elif algo_entry["id"] == "hmac":
        import algorithms.hmac_tool as ht
        settings["algorithm"] = st.selectbox("Hash Algorithm", ht.ALGORITHMS, key="hmac_algo")
        settings["key"] = st.text_input("Secret Key", value="secret-key", key="hmac_key")
        if operation == "verify":
            settings["expected_mac"] = st.text_input("Expected MAC (hex)", key="hmac_expected")

    # --- Encoding ---
    elif algo_entry["id"] == "encoding":
        import algorithms.encoding_tool as et
        settings["algorithm"] = st.selectbox("Encoding Type", list(et.ALGORITHMS.keys()), key="enc_algo")

    # --- Token ---
    elif algo_entry["id"] == "token":
        import algorithms.token_tool as tt
        settings["token_type"] = st.selectbox("Token Type", list(tt.TOKEN_TYPES.keys()), key="tok_type")
        settings["length"] = st.slider("Length (bytes/chars)", 8, 128, 32, key="tok_len")
        settings["count"] = st.slider("Count", 1, 10, 1, key="tok_count")

    # --- Classical Ciphers ---
    elif algo_entry["id"] == "classical":
        import algorithms.classical_tool as ct
        cipher_names = list(ct.CIPHER_CATALOGUE.keys())
        selected_cipher = st.selectbox("Cipher", cipher_names, key="classical_cipher")
        settings["cipher"] = selected_cipher
        info = ct.CIPHER_CATALOGUE.get(selected_cipher, {})

        # Show cipher era and category as context
        era = info.get("era", "")
        cat = info.get("cat", "")
        if era or cat:
            st.caption(f"{cat} | {era}")

        key_type = info.get("key_type", "none")

        if key_type == "int":
            default_k = info.get("key_default", 3)
            if selected_cipher == "Caesar":
                settings["int_key"] = st.slider("Shift (1-25)", 1, 25, default_k, key="classical_int_key")
            elif selected_cipher in ("Railfence", "Scytale"):
                settings["int_key"] = st.slider("Key (rails/rod)", 2, 12, default_k, key="classical_int_key")
            else:
                settings["int_key"] = st.number_input("Integer Key", min_value=1, value=default_k, key="classical_int_key")

        elif key_type == "word":
            default_k = info.get("key_default", "KEY")
            settings["word_key"] = st.text_input(
                f"Keyword", value=default_k, key="classical_word_key",
                help=info.get("key_help", "")
            ).upper().strip()

        elif key_type == "str26":
            default_k = info.get("key_default", "QWERTYUIOPASDFGHJKLZXCVBNM")
            settings["str26_key"] = st.text_input(
                "26-char key alphabet", value=default_k, key="classical_str26_key",
                help="All 26 unique letters in any order"
            ).upper().strip()

        elif key_type == "digits":
            default_k = info.get("key_default", "1234")
            settings["digits_key"] = st.text_input(
                "Digit key", value=default_k, key="classical_digits_key",
                help=info.get("key_help", "")
            ).strip()

        elif key_type == "affine":
            col_a, col_b = st.columns(2)
            with col_a:
                settings["affine_a"] = st.selectbox(
                    "a (coprime to 26)", ct.VALID_AFFINE_A,
                    index=ct.VALID_AFFINE_A.index(5), key="classical_affine_a"
                )
            with col_b:
                settings["affine_b"] = st.slider("b (0-25)", 0, 25, 8, key="classical_affine_b")

        elif key_type == "word_period":
            default_k = info.get("key_default", "KEYWORD")
            settings["word_key"] = st.text_input(
                "Keyword", value=default_k, key="classical_word_key",
                help="Alphabetic keyword for the 5x5 grid"
            ).upper().strip()
            settings["period"] = st.slider("Period", 2, 20, info.get("period_default", 5), key="classical_period")

        elif key_type == "none":
            st.caption("No key required for this cipher.")

        # Playfair note
        if selected_cipher == "Playfair":
            st.info("Playfair: J is treated as I. Double letters are separated with X. Output may be slightly longer than input.")

        # Fill defaults for unused key fields
        settings.setdefault("int_key", 3)
        settings.setdefault("word_key", "KEY")
        settings.setdefault("str26_key", "QWERTYUIOPASDFGHJKLZXCVBNM")
        settings.setdefault("digits_key", "1234")
        settings.setdefault("affine_a", 5)
        settings.setdefault("affine_b", 8)
        settings.setdefault("period", 5)

    return settings


def _render_visualization(algo_entry: dict, text: str, settings: dict) -> None:
    mod = algo_entry["module"]
    if not algo_entry["supports_viz"]:
        return
    if not hasattr(mod, "get_visualization_steps"):
        return
    try:
        steps = mod.get_visualization_steps(text, settings)
        if steps:
            st.markdown("**Transformation Pipeline**")
            pipeline_viz(steps)
    except Exception:
        pass


def _render_hash_comparison_chart(text: str) -> None:
    try:
        import algorithms.hash_tool as ht
        import plotly.graph_objects as go
        results = ht.hash_all(text)
        names = list(results.keys())
        sizes = [results[n].get("bits", 0) for n in names]
        colors = ["#EF4444" if results[n].get("strength") == "weak" else "#3E7DE0" for n in names]
        fig = go.Figure(go.Bar(
            x=names, y=sizes,
            marker_color=colors,
            text=sizes, textposition="auto",
        ))
        fig.update_layout(
            title="Hash Output Size Comparison (bits)",
            plot_bgcolor="#0C1118", paper_bgcolor="#141A22",
            font_color="#E6EAF0",
            xaxis=dict(gridcolor="#283142"),
            yaxis=dict(title="Bits", gridcolor="#283142"),
            height=320,
            margin=dict(l=40, r=20, t=40, b=40),
        )
        st.plotly_chart(fig, key="hash_size_chart")
    except Exception:
        pass


def render() -> None:
    st.markdown("### Cryptography Lab")
    st.caption("Select an algorithm, configure settings, enter input and run the operation.")

    # ----- Sidebar filters -----
    with st.sidebar:
        st.markdown("**Lab Filters**")
        cats = get_by_category()
        cat_filter = st.selectbox("Category", ["All"] + list(cats.keys()), key="lab_cat_filter")
        search_q = st.text_input("Search algorithm", key="lab_search", placeholder="e.g. sha256")

    all_algos = get_all()
    if cat_filter != "All":
        all_algos = [a for a in all_algos if a["category"] == cat_filter]
    if search_q:
        sq = search_q.lower()
        all_algos = [a for a in all_algos if sq in a["name"].lower() or sq in a["description"].lower()]

    if not all_algos:
        st.warning("No algorithms match your filter.")
        return

    algo_names = [a["name"] for a in all_algos]

    # ---- Favorites / recently used ----
    if "favorites" not in st.session_state:
        st.session_state["favorites"] = []
    if "recent" not in st.session_state:
        st.session_state["recent"] = []

    col_algo, col_fav = st.columns([4, 1])
    with col_algo:
        default_idx = 0
        recent = st.session_state.get("recent", [])
        if recent:
            for r in recent:
                if r in algo_names:
                    default_idx = algo_names.index(r)
                    break
        selected_name = st.selectbox("Algorithm", algo_names, index=default_idx, key="lab_algo_select")

    algo_entry = get_by_name(selected_name)
    if algo_entry is None:
        error_box("Algorithm not found.")
        return

    with col_fav:
        favs = st.session_state["favorites"]
        is_fav = selected_name in favs
        fav_label = ":material/star: Saved" if is_fav else ":material/star_border: Save"
        if st.button(fav_label, key="fav_btn"):
            if is_fav:
                st.session_state["favorites"].remove(selected_name)
            else:
                st.session_state["favorites"].append(selected_name)
            st.rerun()

    # Strength indicator
    strength = algo_entry["strength"]
    color = STRENGTH_COLOR.get(strength, "#9CA6B5")
    st.markdown(
        f'<div style="display:flex;gap:12px;align-items:center;margin-bottom:8px;">'
        f'<span style="color:{color};font-weight:700;font-size:13px;text-transform:uppercase;">{strength.upper()}</span>'
        f'<span style="color:#9CA6B5;font-size:13px;">{algo_entry["description"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if strength in ("legacy", "weak"):
        st.warning(f":material/warning: {algo_entry['name']} is marked {strength.upper()}. Do not use in new systems.")
    if strength == "historical":
        st.warning(f":material/history_edu: {algo_entry['name']} contains historical ciphers. All are broken and provide zero modern security. Educational use only.")

    # Operation selector
    ops = get_available_operations(algo_entry)
    op_display = [OP_LABELS.get(o, o) for o in ops]
    op_idx = st.radio("Operation", op_display, horizontal=True, key="lab_op_radio")
    operation = ops[op_display.index(op_idx)]

    st.markdown("---")

    # Settings + Input columns
    col_settings, col_io = st.columns([1, 2])

    with col_settings:
        st.markdown("**Settings**")
        settings = _get_settings_panel(algo_entry, operation)

    with col_io:
        st.markdown("**Input**")
        placeholder = "Enter text here..." if operation != "generate" else "(Leave blank - tokens are generated)"
        input_text = st.text_area(
            "Input text",
            height=140,
            key="lab_input",
            placeholder=placeholder,
            label_visibility="collapsed",
        )

        run_col, clear_col = st.columns([2, 1])
        with run_col:
            run = st.button(":material/play_arrow: Run", type="primary", key="lab_run")
        with clear_col:
            if st.button(":material/delete: Clear", key="lab_clear"):
                st.session_state["lab_input"] = ""
                if "lab_result" in st.session_state:
                    del st.session_state["lab_result"]
                st.rerun()

    # --- Run ---
    if run:
        text = input_text.strip() if input_text else ""

        if operation not in ("generate",):
            ok, msg = validate_text_input(text if text else " ")
            if not text and operation not in ("generate",):
                if operation != "generate":
                    error_box("Input text is required.")
                    return

        # Validate settings
        if hasattr(algo_entry["module"], "validate_settings"):
            valid, vmsg = algo_entry["module"].validate_settings(settings)
            if not valid:
                error_box(f"Settings error: {vmsg}")
                return

        with st.spinner("Running..."):
            result = run_operation(algo_entry, operation, text, settings)

        st.session_state["lab_result"] = result
        st.session_state["lab_result_algo"] = selected_name
        st.session_state["lab_result_op"] = operation

        # Update recents
        recent = st.session_state.get("recent", [])
        if selected_name in recent:
            recent.remove(selected_name)
        recent.insert(0, selected_name)
        st.session_state["recent"] = recent[:8]

        # History
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].insert(0, {
            "algorithm": selected_name,
            "operation": operation,
            "input_preview": text[:50] if text else "",
            "output_preview": result.get("output", "")[:50],
            "elapsed_ms": result.get("elapsed_ms", 0),
        })
        st.session_state["history"] = st.session_state["history"][:50]

    # --- Output ---
    if "lab_result" in st.session_state:
        result = st.session_state["lab_result"]
        st.markdown("---")
        st.markdown("**Output**")

        if "error" in result:
            error_box(result["error"])
        else:
            output = result.get("output", "")
            st.text_area("Result", value=output, height=120, key="lab_output_area", label_visibility="collapsed")

            dl_col, info_col = st.columns([1, 2])
            with dl_col:
                st.download_button(
                    ":material/download: Download",
                    data=output.encode("utf-8"),
                    file_name=f"cryptolab_{selected_name.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    key="lab_download",
                )

            with info_col:
                elapsed = result.get("elapsed_ms", 0)
                st.caption(f"Completed in {elapsed} ms | Output: {len(output)} chars")
                if result.get("info"):
                    st.info(result["info"])
                if result.get("key_used"):
                    with st.expander("Key used (save this)"):
                        st.code(result["key_used"])

            # Visualization
            if algo_entry["supports_viz"]:
                with st.expander(":material/visibility: Transformation Pipeline"):
                    _render_visualization(algo_entry, input_text or "", settings)

            # Hash-specific extras
            if algo_entry["id"] == "hash" and output:
                with st.expander(":material/bar_chart: Hash Size Comparison"):
                    _render_hash_comparison_chart(input_text or "")

                # Entropy
                try:
                    ent = entropy_estimate(output.encode())
                    st.caption(f"Output entropy: {ent} bits/byte")
                except Exception:
                    pass

    # --- Favorites sidebar section ---
    favs = st.session_state.get("favorites", [])
    if favs:
        with st.sidebar:
            st.markdown("---")
            st.markdown("**Saved Algorithms**")
            for f in favs:
                if st.button(f, key=f"fav_jump_{f}"):
                    if f in algo_names:
                        st.session_state["lab_algo_select"] = algo_names.index(f)
                        st.rerun()

    recent_list = st.session_state.get("recent", [])
    if len(recent_list) > 1:
        with st.sidebar:
            st.markdown("---")
            st.markdown("**Recently Used**")
            for r in recent_list[1:5]:
                st.caption(r)

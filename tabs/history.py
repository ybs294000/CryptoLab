"""
History tab - shows past operations in this session.
"""

import streamlit as st
import json


def render() -> None:
    st.markdown("### Operation History")
    st.caption("All operations performed in this session (not persisted across page reloads).")

    history = st.session_state.get("history", [])

    if not history:
        st.info("No operations yet. Run something in the Lab tab.")
        return

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(":material/delete: Clear History", key="history_clear"):
            st.session_state["history"] = []
            st.rerun()
        st.download_button(
            ":material/download: Export JSON",
            data=json.dumps(history, indent=2),
            file_name="cryptolab_history.json",
            mime="application/json",
            key="history_export",
        )

    with col1:
        st.caption(f"{len(history)} operation(s) recorded")

    st.markdown("---")

    for i, item in enumerate(history):
        algo = item.get("algorithm", "Unknown")
        op = item.get("operation", "")
        elapsed = item.get("elapsed_ms", 0)
        inp = item.get("input_preview", "")
        out = item.get("output_preview", "")

        with st.expander(f"#{i+1}  {algo} / {op}  ({elapsed} ms)", expanded=(i == 0)):
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Input preview**")
                st.code(inp if inp else "(none)" , language=None)
            with cols[1]:
                st.markdown("**Output preview**")
                st.code(out if out else "(none)", language=None)

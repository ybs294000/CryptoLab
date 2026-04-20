"""
Compare tab - run the same input through multiple algorithms and display results.
"""

import streamlit as st
import time
import plotly.graph_objects as go
from core.registry import get_all, get_by_name
from core.engine import run_operation, get_default_operation
from utils.validators import validate_text_input
from utils.text_tools import entropy_estimate


STRENGTH_COLOR = {
    "secure": "#22C55E",
    "legacy": "#F59E0B",
    "weak":   "#EF4444",
    "none":   "#4F8EF7",
    "varies": "#9CA6B5",
}


def render() -> None:
    st.markdown("### Algorithm Comparison")
    st.caption("Run the same input through multiple algorithms and compare outputs side by side.")

    all_algos = get_all()
    algo_names = [a["name"] for a in all_algos]

    # Default selections - pick a variety
    default_pick = [a["name"] for a in all_algos
                    if a["id"] in ("hash", "encoding", "hmac")][:3]

    col1, col2 = st.columns([3, 1])
    with col1:
        input_text = st.text_area(
            "Input Text",
            value="Hello, CryptoLab!",
            height=100,
            key="compare_input",
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_all = st.button(":material/compare: Compare", type="primary", key="compare_run")
        if st.button(":material/delete: Clear", key="compare_clear"):
            if "compare_results" in st.session_state:
                del st.session_state["compare_results"]
            st.rerun()

    selected = st.multiselect(
        "Select algorithms to compare",
        algo_names,
        default=default_pick,
        key="compare_select",
    )

    if run_all:
        if not input_text or not input_text.strip():
            st.error("Please enter input text.")
            return
        if not selected:
            st.error("Please select at least one algorithm.")
            return

        results = []
        for name in selected:
            entry = get_by_name(name)
            if entry is None:
                continue
            op = get_default_operation(entry)
            settings = {}
            if hasattr(entry["module"], "default_settings"):
                settings = entry["module"].default_settings()

            try:
                r = run_operation(entry, op, input_text.strip(), settings)
            except Exception as e:
                r = {"error": str(e)}

            output = r.get("output", "")
            results.append({
                "name": name,
                "category": entry["category"],
                "strength": entry["strength"],
                "operation": op,
                "output": output,
                "error": r.get("error", ""),
                "elapsed_ms": r.get("elapsed_ms", 0),
                "output_len": len(output),
                "entropy": entropy_estimate(output.encode()) if output else 0,
            })

        st.session_state["compare_results"] = results

    # Display results
    if "compare_results" in st.session_state:
        results = st.session_state["compare_results"]
        st.markdown("---")
        st.markdown("**Results**")

        for r in results:
            color = STRENGTH_COLOR.get(r["strength"], "#9CA6B5")
            err_html = f'<span style="color:#EF4444;font-size:12px;">{r["error"]}</span>' if r["error"] else ""
            out_display = r["output"][:200] + ("..." if len(r["output"]) > 200 else "")
            out_html = f'<div class="output-box" style="margin-top:6px;">{out_display}</div>' if r["output"] else err_html

            st.markdown(
                f'<div class="crypto-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
                f'  <b style="font-size:15px;">{r["name"]}</b>'
                f'  <span style="color:{color};font-size:11px;font-weight:700;text-transform:uppercase;">{r["strength"]}</span>'
                f'</div>'
                f'<span style="color:#9CA6B5;font-size:12px;">{r["category"]} &bull; {r["operation"]} &bull; {r["elapsed_ms"]} ms &bull; {r["output_len"]} chars</span>'
                f'{out_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Timing chart
        if len(results) > 1:
            st.markdown("---")
            st.markdown("**Performance Comparison**")
            col_a, col_b = st.columns(2)

            with col_a:
                names = [r["name"] for r in results]
                times = [r["elapsed_ms"] for r in results]
                colors = [STRENGTH_COLOR.get(r["strength"], "#9CA6B5") for r in results]
                fig = go.Figure(go.Bar(
                    x=names, y=times,
                    marker_color=colors,
                    text=[f"{t}ms" for t in times],
                    textposition="auto",
                ))
                fig.update_layout(
                    title="Execution Time (ms)",
                    plot_bgcolor="#0C1118",
                    paper_bgcolor="#141A22",
                    font_color="#E6EAF0",
                    xaxis=dict(gridcolor="#283142"),
                    yaxis=dict(title="ms", gridcolor="#283142"),
                    height=280,
                    margin=dict(l=30, r=10, t=40, b=80),
                )
                fig.update_xaxes(tickangle=30)
                st.plotly_chart(fig, key="compare_timing_chart")

            with col_b:
                lengths = [r["output_len"] for r in results]
                fig2 = go.Figure(go.Bar(
                    x=names, y=lengths,
                    marker_color="#3E7DE0",
                    text=lengths,
                    textposition="auto",
                ))
                fig2.update_layout(
                    title="Output Size (chars)",
                    plot_bgcolor="#0C1118",
                    paper_bgcolor="#141A22",
                    font_color="#E6EAF0",
                    xaxis=dict(gridcolor="#283142"),
                    yaxis=dict(title="chars", gridcolor="#283142"),
                    height=280,
                    margin=dict(l=30, r=10, t=40, b=80),
                )
                fig2.update_xaxes(tickangle=30)
                st.plotly_chart(fig2, key="compare_size_chart")

            # Entropy comparison
            ent_data = [(r["name"], r["entropy"]) for r in results if r["entropy"] > 0]
            if ent_data:
                st.markdown("**Output Entropy (bits/byte)** - higher = more random-looking")
                ent_names = [e[0] for e in ent_data]
                ent_vals = [e[1] for e in ent_data]
                fig3 = go.Figure(go.Bar(
                    x=ent_names, y=ent_vals,
                    marker_color="#4F8EF7",
                    text=[f"{v:.2f}" for v in ent_vals],
                    textposition="auto",
                ))
                fig3.update_layout(
                    plot_bgcolor="#0C1118",
                    paper_bgcolor="#141A22",
                    font_color="#E6EAF0",
                    xaxis=dict(gridcolor="#283142"),
                    yaxis=dict(title="bits/byte", gridcolor="#283142", range=[0, 8]),
                    height=260,
                    margin=dict(l=30, r=10, t=20, b=80),
                )
                fig3.update_xaxes(tickangle=30)
                st.plotly_chart(fig3, key="compare_entropy_chart")

        # Export
        st.markdown("---")
        if st.button(":material/download: Export Comparison as JSON", key="compare_export"):
            import json
            export_data = [
                {k: v for k, v in r.items()} for r in results
            ]
            st.download_button(
                "Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="cryptolab_comparison.json",
                mime="application/json",
                key="compare_download",
            )

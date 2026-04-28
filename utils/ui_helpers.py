"""
Reusable UI component helpers.
"""

import streamlit as st


def show_output_box(label: str, content: str, key_suffix: str = "") -> None:
    st.markdown(f"**{label}**")
    st.markdown(
        f'<div class="output-box">{_escape_html(content)}</div>',
        unsafe_allow_html=True,
    )


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def badge(label: str, style: str) -> str:
    """Return HTML badge string. style: secure | legacy | weak | modern"""
    return f'<span class="badge badge-{style}">{label}</span>'


def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)


def success_box(msg: str, title: str = "") -> None:
    notice_box(msg, kind="success", title=title)


def error_box(msg: str, title: str = "") -> None:
    notice_box(msg, kind="error", title=title)


def warning_box(msg: str, title: str = "") -> None:
    notice_box(msg, kind="warning", title=title)


def info_box(msg: str, title: str = "") -> None:
    notice_box(msg, kind="info", title=title)


def notice_box(msg: str, kind: str = "info", title: str = "") -> None:
    notice_class = {
        "info": "notice-info",
        "warning": "notice-warning",
        "success": "notice-success",
        "error": "notice-error",
    }.get(kind, "notice-info")
    title_html = f'<div class="notice-title">{_escape_html(title)}</div>' if title else ""
    body_html = f'<div class="notice-body">{_escape_html(msg)}</div>'
    st.markdown(
        f'<div class="notice-block {notice_class}">{title_html}{body_html}</div>',
        unsafe_allow_html=True,
    )


def copy_button(text: str, label: str = "Copy to clipboard", key: str = "") -> None:
    escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("\n", "\\n")
    button_id = f"copy_btn_{key}"
    st.markdown(
        f"""
<button onclick="navigator.clipboard.writeText(`{escaped}`)"
  style="background:#1B2230;border:1px solid #283142;border-radius:6px;
         color:#E6EAF0;padding:6px 14px;font-size:13px;cursor:pointer;">
  {label}
</button>
""",
        unsafe_allow_html=True,
    )


def pipeline_viz(steps: list[tuple[str, str]]) -> None:
    """
    Render a simple pipeline visualization.
    steps: list of (label, value) tuples
    """
    parts = []
    for i, (label, value) in enumerate(steps):
        val_short = value[:60] + "..." if len(value) > 60 else value
        parts.append(
            f'<div class="step-box"><span style="color:#9CA6B5;font-size:11px;">{label}</span><br>{_escape_html(val_short)}</div>'
        )
        if i < len(steps) - 1:
            parts.append('<span style="color:#3E7DE0;font-size:18px;">&#8594;</span>')

    html = '<div class="step-arrow">' + "".join(parts) + "</div>"
    st.markdown(html, unsafe_allow_html=True)

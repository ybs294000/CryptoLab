"""
Shared branding helpers for CryptoLab.
"""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo1.png"


@st.cache_data
def get_base64_image(path: str) -> str:
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()


def get_logo_base64() -> str:
    if not LOGO_PATH.exists():
        return ""
    return get_base64_image(str(LOGO_PATH))


def render_brand_header(title: str, subtitle: str, *, compact: bool = False) -> None:
    logo_base64 = get_logo_base64()
    image_html = (
        f'<img src="data:image/png;base64,{logo_base64}" width="62" '
        f'style="display:block;object-fit:contain;">'
        if logo_base64
        else ""
    )

    title_size = "2.1rem" if compact else "2.8rem"
    subtitle_size = "0.98rem" if compact else "1.08rem"
    wrap_margin = "18px" if compact else "10px"
    logo_shell = "76px" if compact else "84px"
    logo_radius = "20px" if compact else "22px"

    st.markdown(
        f"""
<div style="display:flex;justify-content:center;align-items:center;gap:14px;margin-bottom:{wrap_margin};">
  <div style="width:{logo_shell};height:{logo_shell};display:flex;justify-content:center;align-items:center;border-radius:{logo_radius};background:rgba(79,142,247,0.12);border:1px solid rgba(79,142,247,0.25);">
    {image_html}
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-start;">
    <h1 style="margin:0;font-size:{title_size};background:linear-gradient(135deg,#4F8EF7 0%,#60A5FA 50%,#93C5FD 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
      {title}
    </h1>
    <h3 style="margin:4px 0 0 0;color:#9BA3B0;font-weight:400;font-size:{subtitle_size};">
      {subtitle}
    </h3>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.divider()


def render_sidebar_brand(version: str) -> None:
    logo_base64 = get_logo_base64()
    image_html = (
        f'<img src="data:image/png;base64,{logo_base64}" width="34" '
        f'style="display:block;object-fit:contain;">'
        if logo_base64
        else ""
    )

    st.markdown(
        f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
  <div style="width:46px;height:46px;display:flex;justify-content:center;align-items:center;border-radius:14px;background:rgba(79,142,247,0.12);border:1px solid rgba(79,142,247,0.24);">
    {image_html}
  </div>
  <div>
    <div style="font-size:1.2rem;font-weight:700;color:#E6EAF0;line-height:1.2;">CryptoLab</div>
    <div style="font-size:12px;color:#9CA6B5;line-height:1.2;">{version}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

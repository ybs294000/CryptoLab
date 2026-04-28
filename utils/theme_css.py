"""
CSS injection for CryptoLab using a dark professional palette.
"""

from __future__ import annotations

import streamlit as st

_P = {
    "primary": "#3E7DE0",
    "primary_hover": "#2F6CD0",
    "accent_bright": "#4F8EF7",
    "bg_main": "#0C1118",
    "bg_card": "#141A22",
    "bg_input": "#1B2230",
    "bg_sunken": "#0F1923",
    "border": "#283142",
    "border_subtle": "#1A2230",
    "text_main": "#E6EAF0",
    "text_muted": "#9CA6B5",
    "text_disabled": "#4A5568",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#4F8EF7",
}


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    try:
        return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"
    except Exception:
        return "62, 125, 224"


def inject_styles() -> None:
    t = _P
    pr = _rgb(t["primary"])

    css = f"""
<style>
:root {{
  --primary: {t["primary"]};
  --primary-hover: {t["primary_hover"]};
  --accent-bright: {t["accent_bright"]};
  --bg-main: {t["bg_main"]};
  --bg-card: {t["bg_card"]};
  --bg-input: {t["bg_input"]};
  --bg-sunken: {t["bg_sunken"]};
  --border: {t["border"]};
  --border-subtle: {t["border_subtle"]};
  --text-main: {t["text_main"]};
  --text-muted: {t["text_muted"]};
  --text-disabled: {t["text_disabled"]};
  --success: {t["success"]};
  --warning: {t["warning"]};
  --error: {t["error"]};
  --info: {t["info"]};
}}

:root {{
  --primary-color: {t["primary"]};
  --background-color: {t["bg_main"]};
  --secondary-background-color: {t["bg_card"]};
  --text-color: {t["text_main"]};
  --text-color-secondary: {t["text_muted"]};
  --border-color: {t["border"]};
  --link-color: {t["accent_bright"]};
}}

.stApp, [data-testid='stAppViewContainer'] {{
  background-color: {t["bg_main"]} !important;
  color: {t["text_main"]} !important;
}}

[data-testid='stMain'] {{
  background-color: {t["bg_main"]} !important;
}}

[data-testid='stSidebar'] {{
  background-color: {t["bg_card"]} !important;
  border-right: 1px solid {t["border"]} !important;
}}

[data-testid='stSidebar'] .stNumberInput > div > div,
[data-testid='stSidebar'] .stSelectbox > div > div,
[data-testid='stSidebar'] .stMultiSelect > div > div {{
  background-color: {t["bg_input"]} !important;
}}

h1 {{
  color: var(--primary) !important;
  letter-spacing: -0.5px;
}}

h2, h3 {{
  color: var(--text-main) !important;
}}

h4, h5, h6 {{
  color: var(--text-muted) !important;
}}

p, li, span, div {{
  color: var(--text-main) !important;
}}

[data-baseweb='tab-list'] {{
  background-color: var(--bg-card) !important;
  border-radius: 8px !important;
  padding: 4px !important;
  gap: 12px !important;
  border: 1px solid var(--border) !important;
  margin-bottom: 16px !important;
}}

button[data-baseweb='tab'] {{
  background: transparent !important;
  border-radius: 6px !important;
  color: var(--text-muted) !important;
  transition: color 0.2s ease !important;
  padding: 6px 14px !important;
}}

button[data-baseweb='tab'][aria-selected='true'] {{
  background-color: var(--primary) !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
}}

button[data-baseweb='tab'] > div[data-testid='stMarkdownContainer'] > p {{
  font-size: 17px !important;
  font-weight: 500 !important;
}}

[data-baseweb='tab-highlight'] {{
  display: none !important;
}}

.stNumberInput > div > div,
.stSelectbox > div > div,
.stMultiSelect > div > div {{
  background-color: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text-main) !important;
}}

.stNumberInput input,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
  background-color: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text-main) !important;
}}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div:focus-within,
.stSelectbox > div > div:focus-within {{
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba({pr}, 0.25) !important;
}}

label, .stLabel, [data-testid='stWidgetLabel'] {{
  color: var(--text-muted) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}}

.stButton > button[kind='primary'],
.stButton > button[data-testid*='primary'] {{
  background-color: var(--primary) !important;
  border: none !important;
  border-radius: 6px !important;
  color: #ffffff !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  transition: background-color 0.2s ease !important;
}}

.stButton > button[kind='primary']:hover,
.stButton > button[data-testid*='primary']:hover {{
  background-color: var(--primary-hover) !important;
}}

.stButton > button,
.stDownloadButton > button {{
  background-color: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text-main) !important;
  font-weight: 500 !important;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
  border-color: var(--primary) !important;
  color: var(--primary) !important;
}}

[data-testid='stMetric'] {{
  background-color: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 14px 18px !important;
}}

[data-testid='stMetricLabel'] {{
  color: var(--text-muted) !important;
}}

[data-testid='stMetricValue'] {{
  color: var(--primary) !important;
  font-weight: 700 !important;
}}

[data-testid='stAlert'] {{
  border-radius: 10px !important;
  border: 1px solid var(--border) !important;
  overflow: hidden !important;
}}

[data-testid='stAlert'] p,
[data-testid='stAlert'] div,
[data-testid='stAlert'] span {{
  color: var(--text-main) !important;
}}

[data-testid='stAlertContentInfo'] {{
  background-color: rgba(79, 142, 247, 0.12) !important;
  border-left: 4px solid var(--info) !important;
}}

[data-testid='stAlertContentWarning'] {{
  background-color: rgba(245, 158, 11, 0.12) !important;
  border-left: 4px solid var(--warning) !important;
}}

[data-testid='stAlertContentError'] {{
  background-color: rgba(239, 68, 68, 0.12) !important;
  border-left: 4px solid var(--error) !important;
}}

[data-testid='stAlertContentSuccess'] {{
  background-color: rgba(34, 197, 94, 0.12) !important;
  border-left: 4px solid var(--success) !important;
}}

[data-testid='stExpander'] details {{
  background-color: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}}

[data-testid='stExpander'] summary {{
  color: var(--text-main) !important;
}}

[data-testid='stCode'],
code,
pre {{
  background-color: var(--bg-sunken) !important;
  color: var(--text-main) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
}}

[data-testid='stDataFrame'] th,
.stDataFrame th {{
  background-color: var(--bg-card) !important;
  color: var(--text-muted) !important;
  border-color: var(--border) !important;
}}

[data-testid='stFileUploader'] {{
  background-color: var(--bg-card) !important;
  border: 2px dashed var(--border) !important;
  border-radius: 8px !important;
  padding: 16px 18px !important;
}}

[data-testid='stFileUploader'] > div {{
  margin-top: 6px !important;
}}

[data-testid='stFileUploader']:hover {{
  border-color: var(--primary) !important;
}}

hr {{
  border-color: var(--border) !important;
  opacity: 0.7 !important;
}}

.stCaption,
small {{
  color: var(--text-muted) !important;
}}

[data-testid='stSlider'] [role='slider'] {{
  background-color: var(--primary) !important;
  border-color: var(--primary) !important;
}}

[data-testid='stSlider'] [role='slider']:focus {{
  box-shadow: 0 0 0 4px rgba({pr}, 0.30) !important;
  outline: none !important;
}}

[data-testid='stSliderThumbValue'] {{
  color: var(--text-main) !important;
}}

[data-testid='stSliderTickBar'] {{
  color: var(--text-muted) !important;
}}

[data-baseweb='popover'] [data-baseweb='menu'],
[data-baseweb='popover'] ul,
[data-baseweb='tooltip'] {{
  background-color: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-main) !important;
}}

[data-baseweb='popover'] [role='option']:hover,
[data-baseweb='popover'] [aria-selected='true'] {{
  background-color: var(--bg-input) !important;
}}

::-webkit-scrollbar {{
  width: 6px;
  height: 6px;
}}

::-webkit-scrollbar-track {{
  background: var(--bg-main);
}}

::-webkit-scrollbar-thumb {{
  background: var(--border);
  border-radius: 3px;
}}

::-webkit-scrollbar-thumb:hover {{
  background: var(--primary);
}}

.crypto-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
  margin-bottom: 12px;
  transition: box-shadow 0.2s ease;
}}

.crypto-card:hover {{
  box-shadow: 0 2px 16px rgba({pr}, 0.18);
  border-color: var(--primary);
}}

.feature-card-blue {{
  background: rgba(79, 142, 247, 0.12);
  border: 1px solid var(--border);
  border-left: 4px solid var(--info);
}}

.feature-card-blue:hover {{
  border-color: var(--accent-bright);
  box-shadow: 0 2px 16px rgba({pr}, 0.16);
}}

.soft-panel {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
}}

.subtle-grid {{
  background-image:
    linear-gradient(rgba(255,255,255,0.012) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.012) 1px, transparent 1px);
  background-size: 24px 24px;
}}

.badge {{
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}

.badge-secure {{ background: rgba(34,197,94,0.15); color: var(--success); border: 1px solid var(--success); }}
.badge-legacy {{ background: rgba(245,158,11,0.15); color: var(--warning); border: 1px solid var(--warning); }}
.badge-weak {{ background: rgba(239,68,68,0.15); color: var(--error); border: 1px solid var(--error); }}
.badge-modern {{ background: rgba(79,142,247,0.15); color: var(--info); border: 1px solid var(--info); }}

.output-box {{
  background: var(--bg-sunken);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--text-main);
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}}

.step-arrow {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
  flex-wrap: wrap;
}}

.step-box {{
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 12px;
  font-family: monospace;
  color: var(--text-main);
  max-width: 280px;
  word-break: break-all;
}}

.info-row {{
  display: flex;
  gap: 8px;
  align-items: baseline;
  margin-bottom: 6px;
  flex-wrap: wrap;
}}

.info-label {{
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
  min-width: 110px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}

.info-value {{
  color: var(--text-main);
  font-size: 13px;
}}

.notice-block {{
  border-radius: 12px;
  padding: 14px 16px;
  margin: 10px 0;
  border: 1px solid var(--border);
}}

.notice-title {{
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 6px;
}}

.notice-body {{
  color: var(--text-main);
  font-size: 14px;
  line-height: 1.65;
}}

.notice-info {{
  background: rgba(79, 142, 247, 0.12);
  border-left: 4px solid var(--info);
}}

.notice-warning {{
  background: rgba(79, 142, 247, 0.12);
  border-left: 4px solid var(--warning);
}}

.notice-success {{
  background: rgba(34, 197, 94, 0.12);
  border-left: 4px solid var(--success);
}}

.notice-error {{
  background: rgba(239, 68, 68, 0.12);
  border-left: 4px solid var(--error);
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

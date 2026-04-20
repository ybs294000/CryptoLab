"""
CSS injection for CryptoLab using the Dark Professional palette.
"""

import streamlit as st

_P = {
    "primary":        "#3E7DE0",
    "primary_hover":  "#2F6CD0",
    "accent_bright":  "#4F8EF7",
    "bg_main":        "#0C1118",
    "bg_card":        "#141A22",
    "bg_input":       "#1B2230",
    "bg_sunken":      "#0F1923",
    "border":         "#283142",
    "border_subtle":  "#1A2230",
    "text_main":      "#E6EAF0",
    "text_muted":     "#9CA6B5",
    "text_disabled":  "#4A5568",
    "success":        "#22C55E",
    "warning":        "#F59E0B",
    "error":          "#EF4444",
    "info":           "#4F8EF7",
}


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    try:
        return f"{int(h[0:2],16)}, {int(h[2:4],16)}, {int(h[4:6],16)}"
    except Exception:
        return "62, 125, 224"


def inject_styles() -> None:
    t = _P
    pr = _rgb(t["primary"])

    css = f"""
<style>
:root {{
  --primary:        {t["primary"]};
  --primary-hover:  {t["primary_hover"]};
  --accent-bright:  {t["accent_bright"]};
  --bg-main:        {t["bg_main"]};
  --bg-card:        {t["bg_card"]};
  --bg-input:       {t["bg_input"]};
  --bg-sunken:      {t["bg_sunken"]};
  --border:         {t["border"]};
  --text-main:      {t["text_main"]};
  --text-muted:     {t["text_muted"]};
  --success:        {t["success"]};
  --warning:        {t["warning"]};
  --error:          {t["error"]};
  --info:           {t["info"]};
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

[data-testid='stSidebar'] .stSelectbox > div > div,
[data-testid='stSidebar'] .stMultiSelect > div > div {{
  background-color: {t["bg_input"]} !important;
}}

h1 {{ color: {t["primary"]} !important; letter-spacing: -0.5px; }}
h2, h3 {{ color: {t["text_main"]} !important; }}
h4, h5, h6 {{ color: {t["text_muted"]} !important; }}

[data-baseweb='tab-list'] {{
  background-color: {t["bg_card"]} !important;
  border-radius: 8px !important;
  padding: 6px 8px !important;
  gap: 16px !important;
  border: 1px solid {t["border"]} !important;
  margin-bottom: 16px !important;
}}

button[data-baseweb='tab'] {{
  background: transparent !important;
  border-radius: 6px !important;
  color: {t["text_muted"]} !important;
  transition: color 0.2s ease !important;
  padding: 6px 14px !important;
}}

button[data-baseweb='tab'][aria-selected='true'] {{
  color: #FFFFFF !important;
  font-weight: 600 !important;
  background-color: {t["primary"]} !important;
}}

button[data-baseweb='tab'] > div[data-testid='stMarkdownContainer'] > p {{
  font-size: 14px !important;
  font-weight: 500 !important;
}}

.stNumberInput > div > div,
.stSelectbox > div > div,
.stMultiSelect > div > div {{
  background-color: {t["bg_input"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 6px !important;
  color: {t["text_main"]} !important;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
  background-color: {t["bg_input"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 6px !important;
  color: {t["text_main"]} !important;
}}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
  border-color: {t["primary"]} !important;
  box-shadow: 0 0 0 2px rgba({pr}, 0.25) !important;
}}

label, .stLabel, [data-testid='stWidgetLabel'] {{
  color: {t["text_muted"]} !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}}

.stButton > button[kind='primary'] {{
  background-color: {t["primary"]} !important;
  border: none !important;
  border-radius: 6px !important;
  color: #ffffff !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  transition: background-color 0.2s ease !important;
}}

.stButton > button[kind='primary']:hover {{
  background-color: {t["primary_hover"]} !important;
}}

.stButton > button,
.stDownloadButton > button {{
  background-color: {t["bg_input"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 6px !important;
  color: {t["text_main"]} !important;
  font-weight: 500 !important;
}}

.stButton > button:hover,
.stDownloadButton > button:hover {{
  border-color: {t["primary"]} !important;
  color: {t["primary"]} !important;
}}

[data-testid='stMetric'] {{
  background-color: {t["bg_card"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 8px !important;
  padding: 14px 18px 10px 18px !important;
}}

[data-testid='stMetric']:hover {{
  box-shadow: 0 2px 12px rgba({pr}, 0.15) !important;
}}

[data-testid='stMetricLabel'] {{ color: {t["text_muted"]} !important; font-size: 0.78rem !important; text-transform: uppercase !important; letter-spacing: 0.04em !important; }}
[data-testid='stMetricValue'] {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 1.45rem !important; }}

[data-testid='stExpander'] details {{
  background-color: {t["bg_card"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 8px !important;
}}

[data-testid='stExpander'] summary {{
  color: {t["text_main"]} !important;
}}

[data-testid='stCode'], code, pre {{
  background-color: {t["bg_sunken"]} !important;
  color: {t["text_main"]} !important;
  border: 1px solid {t["border"]} !important;
  border-radius: 6px !important;
}}

[data-testid='stDataFrame'] th, .stDataFrame th {{
  background-color: {t["bg_card"]} !important;
  color: {t["text_muted"]} !important;
  border-color: {t["border"]} !important;
}}

[data-testid='stFileUploader'] {{
  background-color: {t["bg_card"]} !important;
  border: 2px dashed {t["border"]} !important;
  border-radius: 8px !important;
}}

[data-testid='stFileUploader']:hover {{
  border-color: {t["primary"]} !important;
}}

hr {{ border-color: {t["border"]} !important; opacity: 0.7 !important; }}

.stCaption, small {{ color: {t["text_muted"]} !important; }}

[data-testid='stSlider'] [role='slider'] {{
  background-color: {t["primary"]} !important;
  border-color: {t["primary"]} !important;
}}

[data-baseweb='popover'] [data-baseweb='menu'],
[data-baseweb='popover'] ul {{
  background-color: {t["bg_card"]} !important;
  border: 1px solid {t["border"]} !important;
  color: {t["text_main"]} !important;
}}

[data-baseweb='popover'] [role='option']:hover,
[data-baseweb='popover'] [aria-selected='true'] {{
  background-color: {t["bg_input"]} !important;
}}

::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {t["bg_main"]}; }}
::-webkit-scrollbar-thumb {{ background: {t["border"]}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {t["primary"]}; }}

.crypto-card {{
  background: {t["bg_card"]};
  border: 1px solid {t["border"]};
  border-radius: 10px;
  padding: 18px 20px;
  margin-bottom: 12px;
  transition: box-shadow 0.2s;
}}

.crypto-card:hover {{
  box-shadow: 0 2px 16px rgba({pr}, 0.18);
  border-color: {t["primary"]};
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

.badge-secure {{ background: rgba(34,197,94,0.15); color: {t["success"]}; border: 1px solid {t["success"]}; }}
.badge-legacy {{ background: rgba(245,158,11,0.15); color: {t["warning"]}; border: 1px solid {t["warning"]}; }}
.badge-weak   {{ background: rgba(239,68,68,0.15);  color: {t["error"]};   border: 1px solid {t["error"]}; }}
.badge-modern {{ background: rgba(79,142,247,0.15); color: {t["info"]};    border: 1px solid {t["info"]}; }}

.output-box {{
  background: {t["bg_sunken"]};
  border: 1px solid {t["border"]};
  border-radius: 8px;
  padding: 14px 16px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: {t["text_main"]};
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}}

.step-arrow {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}}

.step-box {{
  background: {t["bg_input"]};
  border: 1px solid {t["border"]};
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 12px;
  font-family: monospace;
  color: {t["text_main"]};
  max-width: 280px;
  word-break: break-all;
}}

.info-row {{
  display: flex;
  gap: 8px;
  align-items: baseline;
  margin-bottom: 6px;
}}

.info-label {{
  color: {t["text_muted"]};
  font-size: 12px;
  font-weight: 600;
  min-width: 110px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}

.info-value {{
  color: {t["text_main"]};
  font-size: 13px;
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

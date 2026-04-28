"""
CryptoLab - Educational Cryptography Platform
Entry point. Keeps main file clean - all logic in tabs/.
"""

import streamlit as st
from utils.branding import LOGO_PATH, render_sidebar_brand

st.set_page_config(
    page_title="CryptoLab",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else ":material/security:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS injection must happen after set_page_config
from utils.theme_css import inject_styles
inject_styles()
from utils.ui_helpers import error_box

# Tab modules
import tabs.home    as tab_home
import tabs.lab     as tab_lab
import tabs.compare as tab_compare
import tabs.batch   as tab_batch
import tabs.learn   as tab_learn
import tabs.history as tab_history
import tabs.about   as tab_about


def main() -> None:
    # Sidebar global info
    with st.sidebar:
        render_sidebar_brand("v1.1.0")
        st.markdown("---")
        st.caption("Educational cryptography platform.")
        st.caption("All operations use real library-backed implementations.")

    # Tab navigation
    tabs = st.tabs([
        ":material/home: Home",
        ":material/science: Lab",
        ":material/compare: Compare",
        ":material/upload_file: Batch",
        ":material/school: Learn",
        ":material/history: History",
        ":material/info: About",
    ])

    with tabs[0]:
        try:
            tab_home.render()
        except Exception as e:
            error_box(f"Home tab error: {e}", title="Home Tab Error")

    with tabs[1]:
        try:
            tab_lab.render()
        except Exception as e:
            error_box(f"Lab tab error: {e}", title="Lab Tab Error")

    with tabs[2]:
        try:
            tab_compare.render()
        except Exception as e:
            error_box(f"Compare tab error: {e}", title="Compare Tab Error")

    with tabs[3]:
        try:
            tab_batch.render()
        except Exception as e:
            error_box(f"Batch tab error: {e}", title="Batch Tab Error")

    with tabs[4]:
        try:
            tab_learn.render()
        except Exception as e:
            error_box(f"Learn tab error: {e}", title="Learn Tab Error")

    with tabs[5]:
        try:
            tab_history.render()
        except Exception as e:
            error_box(f"History tab error: {e}", title="History Tab Error")

    with tabs[6]:
        try:
            tab_about.render()
        except Exception as e:
            error_box(f"About tab error: {e}", title="About Tab Error")

    st.markdown("---")
    st.markdown(
        """
<div style="text-align:center;padding:10px 0 18px 0;color:var(--text-muted);font-size:13px;">
  CryptoLab v1.1.0 • Educational cryptography workspace • Local session processing
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

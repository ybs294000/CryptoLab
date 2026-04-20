"""
CryptoLab - Educational Cryptography Platform
Entry point. Keeps main file clean - all logic in tabs/.
"""

import streamlit as st

st.set_page_config(
    page_title="CryptoLab",
    page_icon=":material/security:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS injection must happen after set_page_config
from utils.theme_css import inject_styles
inject_styles()

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
        st.markdown(
            '<h2 style="margin-bottom:2px;">CryptoLab</h2>'
            '<p style="color:#9CA6B5;font-size:12px;margin-top:0;">v1.0.0</p>',
            unsafe_allow_html=True,
        )
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
            st.error(f"Home tab error: {e}")

    with tabs[1]:
        try:
            tab_lab.render()
        except Exception as e:
            st.error(f"Lab tab error: {e}")

    with tabs[2]:
        try:
            tab_compare.render()
        except Exception as e:
            st.error(f"Compare tab error: {e}")

    with tabs[3]:
        try:
            tab_batch.render()
        except Exception as e:
            st.error(f"Batch tab error: {e}")

    with tabs[4]:
        try:
            tab_learn.render()
        except Exception as e:
            st.error(f"Learn tab error: {e}")

    with tabs[5]:
        try:
            tab_history.render()
        except Exception as e:
            st.error(f"History tab error: {e}")

    with tabs[6]:
        try:
            tab_about.render()
        except Exception as e:
            st.error(f"About tab error: {e}")


if __name__ == "__main__":
    main()

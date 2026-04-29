"""
User-facing About tab.
"""

import streamlit as st

from core.registry import get_all, get_by_category
from utils.branding import render_brand_header
from utils.ui_helpers import info_box, warning_box

APP_VERSION = "1.3.0"


def _metric_row() -> None:
    all_algos = get_all()
    cats = get_by_category()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Version", APP_VERSION)
    col2.metric("Algorithm Families", len(all_algos))
    col3.metric("Categories", len(cats))
    col4.metric("License", "MIT")


def _category_cards() -> None:
    st.markdown("### :material/explore: What You Can Explore")
    cats = get_by_category()
    for cat_name, entries in cats.items():
        names = ", ".join(e["name"] for e in entries)
        st.markdown(
            f"""
<div class="crypto-card">
  <div style="font-size:16px;font-weight:700;margin-bottom:6px;">{cat_name}</div>
  <div style="color:#9CA6B5;font-size:13px;line-height:1.55;">{names}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def _journey_cards() -> None:
    cards = [
        (
            "Lab",
            "Experiment with one algorithm at a time, adjust settings, and inspect the output closely.",
        ),
        (
            "Batch",
            "Process text files or protect images and documents with authenticated encryption.",
        ),
        (
            "Compare",
            "See how multiple algorithms behave on the same input, including output size and timing.",
        ),
        (
            "Learn",
            "Read clear explanations, historical context, and practical guidance on what is secure today.",
        ),
        (
            "Study",
            "Use quizzes and flashcards to reinforce concepts, key handling, and algorithm selection.",
        ),
    ]

    st.markdown("### :material/near_me: Where To Start")
    first_row = st.columns(2)
    second_row = st.columns(2)
    third_row = st.columns(1)
    all_columns = [first_row[0], first_row[1], second_row[0], second_row[1], third_row[0]]

    for col, (title, body) in zip(all_columns, cards):
        with col:
            st.markdown(
                f"""
<div class="crypto-card feature-card-blue" style="min-height:120px;">
  <div style="font-size:18px;font-weight:700;margin-bottom:10px;">{title}</div>
  <div style="color:var(--text-muted);font-size:14px;line-height:1.65;">{body}</div>
</div>
""",
                unsafe_allow_html=True,
            )


def _technical_details() -> None:
    st.markdown("### :material/description: Technical Details")
    st.caption("A plain-language view of how the app is put together and how to work with it.")

    st.markdown("""
**How the app is organized**

- app.py sets up the page shell and routes each top-level tab.
- The tabs folder contains the user workflows such as Lab, Compare, Batch, Learn, History, and About.
- The core registry keeps the catalog of algorithm modules.
- The core engine dispatches the selected operation to the chosen algorithm.
- The data folder stores educational metadata used in the Learn tab.
- The utils folder contains styling, branding, validation, and file helpers.
""")


def _technology_stack() -> None:
    st.markdown("### :material/developer_board: Technologies And Frameworks")
    st.markdown("""
- **Streamlit** powers the app interface and session-driven workflow.
- **PyCryptodome** provides AES and ChaCha20-Poly1305 implementations.
- **cryptography** provides Fernet and related secure primitives.
- **Plotly** is used for comparison charts and visual explainers.
- **pycipher** and **secretpy** provide the historical and classical cipher implementations.
- **Python standard library** supports encoding tools, file packaging, and utility flows.
""")


def _limitations() -> None:
    st.markdown("### :material/report_problem: Current Limitations")
    st.markdown("""
- Maximum text input and upload size is limited to 512 KB in the current configuration.
- Results and history are stored only for the active session and are not saved permanently.
- Classical ciphers operate on letters and are included for learning, not real protection.
- RSA is available for text experimentation, but not for bulk file workflows.
- The secure file workflow protects one file at a time and exports it into a CryptoLab package rather than the original file format.
""")


def _guide() -> None:
    st.markdown("### :material/menu_book: Quick Guide")
    st.markdown("""
1. Start in **Lab** when you want to try one algorithm with full control over settings.
2. Use **Compare** to see how different algorithms behave on the same input.
3. Use **Batch** for text files or for encrypting and decrypting images and business documents.
4. Use **Learn** when you want plain-language explanations before choosing an algorithm.
5. Save any generated encryption key immediately, because decryption depends on that exact key.
""")


def _faq() -> None:
    st.markdown("### :material/live_help: FAQ")
    with st.expander(":material/key: Why do I need to save the generated key?"):
        st.markdown("Auto-generated keys are unique to that encryption run. Without the same key, decryption is not possible later.")
    with st.expander(":material/code: Is encoding the same as encryption?"):
        st.markdown("No. Encoding only changes representation for transport or storage. It does not provide security.")
    with st.expander(":material/folder_managed: Why is a protected file downloaded as a `.cryptolab` package?"):
        st.markdown("The package preserves the encrypted content plus the metadata needed to restore the original file name, type, and required decryption settings.")
    with st.expander(":material/history: Why does the app keep showing my previous output in Lab?"):
        st.markdown("The Lab tab keeps the last successful run visible so you can compare what changed before deciding to run again. Once you press Run, the output updates to the new state.")

    st.markdown("""
**How algorithms are added**

Each algorithm family lives in its own module under the algorithms folder. The app looks for standard fields such as the algorithm name, category, strength label, and supported operations. Once a module is registered, it becomes available across the app automatically.
""")

    st.markdown("""
**How file protection works**

The secure file workflow in the Batch tab uses authenticated encryption so the app can detect tampering during decryption. Encrypted files are exported as CryptoLab secure packages, which preserve the original filename and media type for later restoration.
""")

    st.markdown("""
**Quality checks**

CryptoLab includes automated tests for registry loading, helper utilities, and secure file roundtrips for AES-GCM, ChaCha20-Poly1305, and Fernet. A markdown test report is generated in tests/TEST_REPORT.md when the suite is run.
""")

    st.markdown("""
**Where to look next**

- README.md for the current overview and setup instructions
- CHANGELOG.md for the latest feature summary
- docs/TESTING.md for the test workflow
- docs/THEMING.md for the visual system and theme files
""")


def render() -> None:
    render_brand_header(
        "About CryptoLab",
        "A practical workspace for learning encryption, hashing, encoding, authentication, and secure file protection.",
        compact=True,
    )

    _metric_row()

    st.markdown("---")
    st.markdown("""
### :material/info: What CryptoLab Is

CryptoLab is built to help you understand cryptography by trying it yourself. You can encrypt messages, compare algorithms, inspect outputs, process text files in bulk, and now protect common files such as images and documents with authenticated encryption.

The app keeps educational breadth without losing practicality. It includes modern algorithms you would use in real systems, legacy algorithms you may still encounter, and historical ciphers so the security differences are easy to see.
""")

    st.markdown("---")
    _journey_cards()

    st.markdown("---")
    _category_cards()

    st.markdown("---")
    st.markdown("### :material/gpp_good: Security Guidance")
    warning_box(
        "Use modern authenticated encryption for real files and sensitive data. In this app, the safest choices are AES-GCM, ChaCha20-Poly1305, and Fernet.",
        title="Recommended For Real Use",
    )
    st.markdown("""
- Algorithms marked `LEGACY` are still useful to study, but should not be chosen for new systems.
- Algorithms marked `WEAK` are included so you can understand why they fell out of use.
- Encoding tools are for representation and transport, not security.
- Historical ciphers are for learning only and do not provide meaningful protection.
""")

    st.markdown("---")
    st.markdown("### :material/privacy_tip: Privacy And Handling")
    st.markdown("""
- Operations run locally in your Streamlit session.
- Temporary results stay in session state until you clear or refresh the app.
- If a key is auto-generated for encryption, you need to save it to decrypt later.
- File decryption in the secure file workflow restores the original filename and file type when available.
""")

    st.markdown("---")
    _technology_stack()

    st.markdown("---")
    _limitations()

    st.markdown("---")
    _guide()

    st.markdown("---")
    _faq()

    st.markdown("---")
    with st.expander(":material/description: Technical Details"):
        _technical_details()

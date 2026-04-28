"""
Learn tab - detailed algorithm information from JSON metadata.
"""

import streamlit as st
from core.metadata import load_all_metadata, load_metadata
from core.registry import get_all, get_by_id
import urllib.parse
from utils.ui_helpers import info_box


STRENGTH_BADGE_HTML = {
    "secure":     '<span class="badge badge-secure">SECURE</span>',
    "legacy":     '<span class="badge badge-legacy">LEGACY</span>',
    "weak":       '<span class="badge badge-weak">WEAK</span>',
    "none":       '<span class="badge badge-modern">ENCODING</span>',
    "varies":     '<span class="badge badge-modern">VARIES</span>',
    "historical": '<span class="badge badge-weak">HISTORICAL / BROKEN</span>',
}

CAT_ICONS = {
    "Modern Encryption":  "lock",
    "Legacy Encryption":  "history",
    "Hashing":            "tag",
    "Authentication":     "verified_user",
    "Encoding":           "code",
    "Randomness":         "casino",
    "Other":              "science",
}


def _info_row(label: str, value) -> str:
    if not value:
        return ""
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    return (
        f'<div class="info-row">'
        f'<span class="info-label">{label}</span>'
        f'<span class="info-value">{value}</span>'
        f'</div>'
    )


def _render_algo_card(algo_id: str, algo_entry: dict, meta: dict) -> None:
    strength = algo_entry.get("strength", "unknown")
    badge = STRENGTH_BADGE_HTML.get(strength, "")
    cat_icon = CAT_ICONS.get(algo_entry.get("category", ""), "science")

    header = f":material/{cat_icon}: {algo_entry['name']}"
    with st.expander(header, expanded=False):
        # Badges row
        st.markdown(badge, unsafe_allow_html=True)
        st.markdown(f"*{meta.get('description', algo_entry.get('description', ''))}*")
        st.markdown("---")

        # Info table
        info_html = (
            _info_row("Category", meta.get("category"))
            + _info_row("Introduced", meta.get("introduced"))
            + _info_row("Creator", meta.get("creator"))
            + _info_row("Key Sizes", meta.get("key_sizes"))
            + _info_row("Modern Use", meta.get("modern_use"))
            + _info_row("Breakability", meta.get("breakability"))
        )
        st.markdown(f'<div style="margin-bottom:12px;">{info_html}</div>', unsafe_allow_html=True)

        # Notes
        notes = meta.get("notes", "")
        if notes:
            info_box(notes, title="Notes")

        # Did you know
        dyk = meta.get("did_you_know", "")
        if dyk:
            info_box(dyk, title="Did You Know?")

        # Related algorithms
        related = meta.get("related_algorithms", [])
        if related:
            st.caption(f"Related: {', '.join(related)}")

        # Action buttons
        wiki_url = meta.get("wikipedia_url", "")
        search_q = meta.get("search_query")
        if not search_q:
            search_q = f"{algo_entry['name']} cryptography algorithm"
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(search_q)}"

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if wiki_url:
                st.link_button(":material/open_in_new: Wikipedia", wiki_url)
        with btn_col2:
            st.link_button(":material/search: Google", google_url)


def render() -> None:
    st.markdown("### Learn Cryptography")
    st.caption("Detailed information about each algorithm - history, usage, strengths and weaknesses.")

    all_meta = load_all_metadata()
    all_algos = get_all()

    # Search + filter
    search_q = st.text_input(
        ":material/search: Search algorithms",
        key="learn_search",
        placeholder="e.g. AES, hash, legacy...",
    )

    strength_filter = st.multiselect(
        "Filter by Strength",
        ["secure", "legacy", "weak", "none", "varies"],
        default=[],
        key="learn_strength_filter",
    )

    # Group by category
    from core.registry import get_by_category
    cats = get_by_category()

    shown = 0
    for cat_name, entries in cats.items():
        # Filter
        filtered = []
        for entry in entries:
            if search_q:
                sq = search_q.lower()
                if sq not in entry["name"].lower() and sq not in entry["description"].lower() and sq not in entry["category"].lower():
                    continue
            if strength_filter and entry["strength"] not in strength_filter:
                continue
            filtered.append(entry)

        if not filtered:
            continue

        icon = CAT_ICONS.get(cat_name, "science")
        st.markdown(f"#### :material/{icon}: {cat_name}")

        for entry in filtered:
            meta = all_meta.get(entry["id"], {})
            if not meta:
                # Fallback - use registry info
                meta = {
                    "description": entry.get("description", ""),
                    "category": entry.get("category", ""),
                    "notes": "",
                }
            _render_algo_card(entry["id"], entry, meta)
            shown += 1

        st.markdown("")

    if shown == 0:
        info_box("No algorithms match your search.", title="No Results")

    # Concepts section
    st.markdown("---")
    st.markdown("### Core Concepts")

    with st.expander(":material/info: Encryption vs Hashing vs Encoding"):
        st.markdown("""
**Encryption** transforms data so only authorized parties can read it. It is reversible with the correct key. Examples: AES, RSA, Fernet.

**Hashing** produces a fixed-size fingerprint of data. It is one-way - you cannot reverse a hash to get the original input. Examples: SHA-256, BLAKE2, MD5.

**Encoding** converts data to a different representation for transport or storage. It provides NO security and is trivially reversible. Examples: Base64, Hex, URL encoding.

**Authentication (MAC)** verifies both the integrity of data and its origin. Requires a shared secret key. Examples: HMAC-SHA256.
""")

    with st.expander(":material/key: Symmetric vs Asymmetric Encryption"):
        st.markdown("""
**Symmetric encryption** uses the same key for both encryption and decryption. Fast, suitable for bulk data. Key must be shared securely. Examples: AES, Fernet, ChaCha20.

**Asymmetric encryption** uses a public/private key pair. Encrypt with the public key, decrypt with the private key. Slower, used for key exchange and digital signatures. Examples: RSA, ECC.

In practice, **hybrid encryption** is used: asymmetric crypto to exchange a symmetric key, then symmetric crypto for bulk data (e.g., TLS).
""")

    with st.expander(":material/warning: Why MD5 and SHA-1 Are Broken"):
        st.markdown("""
**MD5** was broken in 2004. Researchers demonstrated that two different inputs could produce the same MD5 hash (a collision). By 2008, attackers used MD5 collisions to create a rogue HTTPS certificate.

**SHA-1** was broken in 2017 with the SHAttered attack by Google researchers. They produced two different PDF files with the same SHA-1 hash, requiring 9.2 quintillion hash computations.

**Practical impact**: Never use MD5 or SHA-1 for security purposes. Acceptable alternatives: SHA-256, SHA-3-256, or BLAKE2.
""")

    with st.expander(":material/security: Authenticated Encryption (AEAD)"):
        st.markdown("""
Standard encryption (e.g., AES-CBC) provides confidentiality but NOT integrity. An attacker could modify the ciphertext and you wouldn't know.

**Authenticated Encryption with Associated Data (AEAD)** combines encryption and authentication:
- **AES-GCM** - AES + GHASH authentication tag
- **ChaCha20-Poly1305** - ChaCha20 + Poly1305 MAC
- **Fernet** - AES-CBC + HMAC-SHA256

AEAD should be the default choice for any new symmetric encryption. If someone modifies the ciphertext, decryption will fail with a verification error.
""")

    with st.expander(":material/history: The History of Classical Ciphers"):
        st.markdown("""
Classical ciphers represent thousands of years of cryptographic thinking, ultimately all defeated as mathematics advanced.

**Substitution ciphers** (replace letters with other letters):

- **Atbash (~600 BC)** - Ancient Hebrew, A=Z B=Y. Broken by inspection.
- **Caesar (~50 BC)** - Shift by 3. Only 25 possible keys. Broken by trying all.
- **Affine (16th c)** - Mathematical generalization of Caesar. Broken by frequency analysis.
- **Vigenere (1553)** - Called "Le Chiffre Indechiffrable" (unbreakable) for 300 years. Broken by Babbage and Kasiski using index of coincidence.
- **Playfair (1854)** - Digraph cipher, used by British in WW1. Broken by frequency analysis of letter pairs.

**Transposition ciphers** (rearrange letters, don't replace them):

- **Scytale (~700 BC)** - Spartan military cipher. Broken by obtaining a rod of the right diameter.
- **Railfence** - Zigzag pattern. Broken with basic pattern analysis.

**Why they all failed**: Small key spaces, mathematical patterns, and frequency analysis. English letters have predictable distributions (E is most common at ~13%). Any monoalphabetic cipher preserves these frequencies in the output, making it trivially breakable.
""")

    with st.expander(":material/bar_chart: English Letter Frequency Analysis"):
        try:
            import plotly.graph_objects as go
            freqs = {
                'E':12.7,'T':9.1,'A':8.2,'O':7.5,'I':7.0,'N':6.7,'S':6.3,'H':6.1,
                'R':6.0,'D':4.3,'L':4.0,'C':2.8,'U':2.8,'M':2.4,'W':2.4,'F':2.2,
                'G':2.0,'Y':2.0,'P':1.9,'B':1.5,'V':1.0,'K':0.8,'J':0.15,'X':0.15,
                'Q':0.10,'Z':0.07
            }
            fig = go.Figure(go.Bar(
                x=list(freqs.keys()),
                y=list(freqs.values()),
                marker_color="#3E7DE0",
                text=[f"{v}%" for v in freqs.values()],
                textposition="outside",
            ))
            fig.update_layout(
                title="English Letter Frequency (%) - the foundation of frequency analysis attacks",
                plot_bgcolor="#0C1118", paper_bgcolor="#141A22",
                font_color="#E6EAF0",
                xaxis=dict(gridcolor="#283142"),
                yaxis=dict(title="%", gridcolor="#283142"),
                height=320,
                margin=dict(l=30, r=10, t=50, b=30),
            )
            st.plotly_chart(fig, key="learn_freq_chart")
            st.caption("Any monoalphabetic substitution cipher (Caesar, Affine, Simple Substitution) preserves this distribution in ciphertext, making it trivially breakable.")
        except Exception:
            info_box("Install plotly to see this chart.", title="Chart Unavailable")

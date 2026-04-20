"""
Home tab - intro, categories, quickstart, did-you-know facts.
"""

import streamlit as st
from core.registry import get_by_category, get_all
from core.metadata import load_all_metadata
import random


STRENGTH_BADGE = {
    "secure":     ('<span class="badge badge-secure">SECURE</span>', "secure"),
    "legacy":     ('<span class="badge badge-legacy">LEGACY</span>', "legacy"),
    "weak":       ('<span class="badge badge-weak">WEAK</span>',     "weak"),
    "none":       ('<span class="badge badge-modern">ENCODING</span>', "modern"),
    "varies":     ('<span class="badge badge-modern">VARIES</span>',  "modern"),
    "historical": ('<span class="badge badge-weak">HISTORICAL</span>', "weak"),
    "unknown":    ('<span class="badge badge-modern">UNKNOWN</span>', "modern"),
}

CAT_ICONS = {
    "Modern Encryption":        "lock",
    "Legacy Encryption":        "history",
    "Hashing":                  "tag",
    "Authentication":           "verified_user",
    "Encoding":                 "code",
    "Randomness":               "casino",
    "Classical (Educational)":  "school",
}

DID_YOU_KNOW = [
    "AES-256 has never been broken. A brute-force attack would take longer than the age of the universe.",
    "SHA-1 was officially deprecated in 2017 after Google produced the first known SHA-1 collision.",
    "RSA was kept secret by British intelligence for 24 years before being independently published.",
    "ChaCha20-Poly1305 replaced RC4 in TLS because RC4 had provable statistical biases.",
    "The Python random module is NOT cryptographically secure - always use secrets for tokens.",
    "Fernet guarantees that messages cannot be manipulated or read without the key.",
    "HMAC-SHA256 signs every single request made to AWS APIs worldwide.",
    "Base64 is encoding, not encryption - it provides zero security.",
    "AES was originally called Rijndael, named after its Belgian inventors.",
    "3DES is still used in some banking systems despite being superseded by AES in 2001.",
    "The Vigenere cipher was considered unbreakable for 300 years until Babbage cracked it in the 1800s.",
    "Caesar cipher has only 25 possible keys - a child could brute-force it by hand.",
    "The Playfair cipher was used by the British in WW1 and WW2, and is broken by digraph frequency analysis.",
    "The Scytale was used by Spartan generals ~700 BC - arguably the first military cipher device.",
    "Atbash (A=Z, B=Y...) is found in the Hebrew Bible and dates to ~600 BC.",
    "The Enigma machine used in WW2 was a polyalphabetic cipher - broken by Alan Turing at Bletchley Park.",
]


def render() -> None:
    # Hero
    st.markdown("""
<div style="text-align:center;padding:32px 0 20px 0;">
  <h1 style="font-size:2.6rem;margin-bottom:6px;">CryptoLab</h1>
  <p style="color:#9CA6B5;font-size:1.1rem;max-width:560px;margin:0 auto;">
    An interactive cryptography learning platform. Experiment with real library-backed
    algorithms, visualize transformations, and understand the difference between
    encoding, hashing, and encryption.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # Stats row
    all_algos = get_all()
    cats = get_by_category()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithms", len(all_algos))
    c2.metric("Categories", len(cats))
    c3.metric("Secure", sum(1 for a in all_algos if a["strength"] == "secure"))
    c4.metric("Legacy / Weak", sum(1 for a in all_algos if a["strength"] in ("legacy", "weak")))

    st.markdown("---")

    # Did you know
    fact = random.choice(DID_YOU_KNOW)
    st.info(f"**Did you know?**  {fact}")

    st.markdown("---")

    # Category overview
    st.markdown("### Available Categories")
    for cat_name, entries in cats.items():
        icon = CAT_ICONS.get(cat_name, "category")
        with st.expander(f":material/{icon}: {cat_name}  ({len(entries)} algorithms)"):
            for algo in entries:
                badge_html, _ = STRENGTH_BADGE.get(algo["strength"], STRENGTH_BADGE["unknown"])
                st.markdown(
                    f'<div class="crypto-card">'
                    f'<b>{algo["name"]}</b> &nbsp; {badge_html}<br>'
                    f'<span style="color:#9CA6B5;font-size:13px;">{algo["description"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # Quick start guide
    st.markdown("### Quick Start")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**Encrypt / Decrypt**
1. Go to the **Lab** tab
2. Select an encryption algorithm (AES, Fernet, etc.)
3. Choose Encrypt mode
4. Enter your text
5. Click **Run** - copy or download the output

**Hash Text**
1. Go to **Lab** tab
2. Select a hash algorithm (SHA-256, etc.)
3. Enter text and click **Run**
""")
    with col2:
        st.markdown("""
**Compare Algorithms**
1. Go to the **Compare** tab
2. Enter input text
3. Select multiple algorithms
4. View all outputs side by side

**Process Files**
1. Go to **Batch** tab
2. Upload a .txt file
3. Choose algorithm and operation
4. Download the processed result
""")

    st.markdown("---")

    # Educational disclaimer
    st.markdown("""
<div style="background:#141A22;border:1px solid #283142;border-radius:8px;padding:16px 20px;">
  <b style="color:#4F8EF7;">Educational Disclaimer</b><br>
  <span style="color:#9CA6B5;font-size:13px;">
  CryptoLab uses real, library-backed cryptographic algorithms for educational purposes.
  All operations use reputable Python libraries (cryptography, pycryptodome, hashlib).
  Do not use this tool as a substitute for professional security review.
  Algorithms marked LEGACY or WEAK should not be used in new systems.
  </span>
</div>
""", unsafe_allow_html=True)

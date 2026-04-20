"""
Metadata loader - reads algorithm detail JSON from data/ directory.
"""

import json
import os
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


@st.cache_data
def load_metadata(algo_id: str) -> dict | None:
    path = os.path.join(DATA_DIR, f"{algo_id}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data
def load_all_metadata() -> dict:
    result = {}
    if not os.path.exists(DATA_DIR):
        return result
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            algo_id = fname[:-5]
            data = load_metadata(algo_id)
            if data:
                result[algo_id] = data
    return result

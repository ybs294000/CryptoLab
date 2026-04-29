"""
Study content loaders and validators for quizzes and flashcards.
"""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


STUDY_DIR = Path(__file__).resolve().parent.parent / "data" / "study"
SCHEMA_PATH = STUDY_DIR / "schema.json"
QUIZ_PATH = STUDY_DIR / "quizzes.json"
FLASHCARD_PATH = STUDY_DIR / "flashcards.json"

SUPPORTED_SCHEMA_COMPONENTS = {
    "hero_card",
    "metric_strip",
    "topic_filter",
    "difficulty_filter",
    "dataset_selector",
    "selection_summary",
    "quiz_player",
    "flashcard_player",
}


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@st.cache_data
def load_study_schema() -> dict:
    return _load_json(SCHEMA_PATH)


@st.cache_data
def load_study_quizzes() -> dict:
    return _load_json(QUIZ_PATH)


@st.cache_data
def load_study_flashcards() -> dict:
    return _load_json(FLASHCARD_PATH)


def validate_study_schema(schema: dict) -> tuple[bool, str]:
    views = schema.get("views")
    if not isinstance(views, list) or not views:
        return False, "Study schema must define at least one view."

    for view in views:
        if not isinstance(view, dict):
            return False, "Each study view must be an object."
        if not view.get("id") or not view.get("label"):
            return False, "Each study view must include id and label."
        components = view.get("components")
        if not isinstance(components, list) or not components:
            return False, f"Study view '{view.get('id', 'unknown')}' must define components."
        for component in components:
            comp_type = component.get("type")
            if comp_type not in SUPPORTED_SCHEMA_COMPONENTS:
                return False, f"Unsupported study schema component: {comp_type}"
    return True, ""


def validate_quiz_content(payload: dict) -> tuple[bool, str]:
    quiz_sets = payload.get("quiz_sets")
    if not isinstance(quiz_sets, list) or not quiz_sets:
        return False, "Quiz content must include at least one quiz set."

    for quiz_set in quiz_sets:
        if not quiz_set.get("id") or not quiz_set.get("title"):
            return False, "Each quiz set must include id and title."
        questions = quiz_set.get("questions")
        if not isinstance(questions, list) or not questions:
            return False, f"Quiz set '{quiz_set.get('id', 'unknown')}' must include questions."
        for question in questions:
            options = question.get("options")
            answer_index = question.get("answer_index")
            if not question.get("prompt"):
                return False, f"Quiz set '{quiz_set['id']}' contains a question without a prompt."
            if not isinstance(options, list) or len(options) < 2:
                return False, f"Quiz question '{question.get('prompt', '')}' must offer at least two options."
            if not isinstance(answer_index, int) or answer_index < 0 or answer_index >= len(options):
                return False, f"Quiz question '{question.get('prompt', '')}' has an invalid answer index."
    return True, ""


def validate_flashcard_content(payload: dict) -> tuple[bool, str]:
    decks = payload.get("decks")
    if not isinstance(decks, list) or not decks:
        return False, "Flashcard content must include at least one deck."

    for deck in decks:
        if not deck.get("id") or not deck.get("title"):
            return False, "Each flashcard deck must include id and title."
        cards = deck.get("cards")
        if not isinstance(cards, list) or not cards:
            return False, f"Flashcard deck '{deck.get('id', 'unknown')}' must include cards."
        for card in cards:
            if not card.get("front") or not card.get("back"):
                return False, f"Flashcard deck '{deck['id']}' contains a card missing front or back text."
    return True, ""

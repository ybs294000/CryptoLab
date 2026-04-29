"""
Study tab - schema-driven quizzes and flashcards.
"""

from __future__ import annotations

import random

import streamlit as st

from core.study_content import (
    load_study_flashcards,
    load_study_quizzes,
    load_study_schema,
    validate_flashcard_content,
    validate_quiz_content,
    validate_study_schema,
)
from utils.branding import render_brand_header
from utils.ui_helpers import error_box, info_box, success_box, warning_box


def _ensure_state() -> None:
    st.session_state.setdefault("study_quiz_results", {})
    st.session_state.setdefault("study_flashcard_index", {})
    st.session_state.setdefault("study_flashcard_face", {})


def _format_template(template: str, context: dict) -> str:
    safe_context = {key: value for key, value in context.items() if isinstance(value, (str, int, float))}
    try:
        return template.format(**safe_context)
    except Exception:
        return template


def _filter_items(items: list[dict], *, topic: str = "All", difficulty: str = "All") -> list[dict]:
    filtered = []
    for item in items:
        if topic != "All" and item.get("topic") != topic:
            continue
        if difficulty != "All" and item.get("difficulty") != difficulty:
            continue
        filtered.append(item)
    return filtered


def _render_hero_card(component: dict) -> None:
    st.markdown(
        f"""
<div class="soft-panel subtle-grid" style="margin-bottom:16px;">
  <div style="font-size:1.08rem;font-weight:700;margin-bottom:6px;">{component.get("title", "")}</div>
  <div style="color:var(--text-muted);font-size:14px;line-height:1.65;">
    {component.get("body", "")}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_metric_strip(component: dict, context: dict) -> None:
    items = component.get("items", [])
    if not items:
        return
    columns = st.columns(len(items))
    for col, item in zip(columns, items):
        value = context.get(item.get("value_key", ""), 0)
        col.metric(item.get("label", "Metric"), value)


def _render_topic_filter(component: dict, context: dict, view_id: str) -> None:
    source = component.get("source", "")
    items = context.get(source, [])
    topics = sorted({item.get("topic", "General") for item in items if item.get("topic")})
    selected = st.selectbox(
        component.get("label", "Topic"),
        ["All"] + topics,
        key=f"study_{view_id}_{source}_topic",
    )
    context[f"{source}_topic"] = selected


def _render_difficulty_filter(component: dict, context: dict, view_id: str) -> None:
    source = component.get("source", "")
    items = context.get(source, [])
    levels = sorted({item.get("difficulty", "General") for item in items if item.get("difficulty")})
    selected = st.selectbox(
        component.get("label", "Difficulty"),
        ["All"] + levels,
        key=f"study_{view_id}_{source}_difficulty",
    )
    context[f"{source}_difficulty"] = selected


def _render_dataset_selector(component: dict, context: dict, view_id: str) -> None:
    source = component.get("source", "")
    items = context.get(source, [])
    topic = context.get(f"{source}_topic", "All")
    difficulty = context.get(f"{source}_difficulty", "All")
    filtered = _filter_items(items, topic=topic, difficulty=difficulty)
    context[f"filtered_{source}"] = filtered
    context["filtered_count"] = len(filtered)

    if not filtered:
        info_box(component.get("empty_message", "No study content is available for the current filters."), title="No Matching Content")
        context[f"selected_{source[:-1]}"] = None
        return

    options = {item["title"]: item for item in filtered}
    selected_title = st.selectbox(
        component.get("label", "Select"),
        list(options.keys()),
        key=f"study_{view_id}_{source}_selector",
    )
    selected_item = options[selected_title]
    singular_name = source[:-1]
    context[f"selected_{singular_name}"] = selected_item


def _render_selection_summary(component: dict, context: dict) -> None:
    template = component.get("template", "")
    if template:
        info_box(_format_template(template, context), title="Current Selection")


def _grade_quiz(quiz_set: dict, responses: dict[str, str]) -> dict:
    details = []
    score = 0
    answered = 0

    for index, question in enumerate(quiz_set.get("questions", []), start=1):
        selected_value = responses.get(str(index), "")
        correct_option = question["options"][question["answer_index"]]
        is_answered = bool(selected_value)
        is_correct = selected_value == correct_option
        if is_answered:
            answered += 1
        if is_correct:
            score += 1
        details.append(
            {
                "number": index,
                "prompt": question["prompt"],
                "selected": selected_value or "Not answered",
                "correct": correct_option,
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
            }
        )

    total = len(quiz_set.get("questions", []))
    return {
        "score": score,
        "total": total,
        "answered": answered,
        "details": details,
    }


def _reset_quiz_attempt(quiz_id: str, total_questions: int) -> None:
    st.session_state["study_quiz_results"].pop(quiz_id, None)
    for index in range(1, total_questions + 1):
        st.session_state[f"study_quiz_{quiz_id}_{index}"] = ""


def _render_quiz_player(context: dict) -> None:
    quiz_set = context.get("selected_quiz_set")
    if not quiz_set:
        return

    quiz_id = quiz_set["id"]
    results = st.session_state["study_quiz_results"].get(quiz_id)

    st.markdown(
        f"""
<div class="crypto-card">
  <div style="font-size:18px;font-weight:700;margin-bottom:6px;">{quiz_set["title"]}</div>
  <div style="color:var(--text-muted);font-size:14px;line-height:1.65;">{quiz_set.get("description", "")}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.form(key=f"study_quiz_form_{quiz_id}"):
        responses: dict[str, str] = {}
        for index, question in enumerate(quiz_set.get("questions", []), start=1):
            responses[str(index)] = st.selectbox(
                f"Q{index}. {question['prompt']}",
                [""] + question["options"],
                key=f"study_quiz_{quiz_id}_{index}",
                format_func=lambda value: "Choose an answer" if value == "" else value,
            )
        submit = st.form_submit_button(":material/quiz: Check Answers", type="primary")

    action_col, _ = st.columns([1, 3])
    with action_col:
        st.button(
            ":material/restart_alt: Reset Quiz",
            key=f"study_quiz_reset_{quiz_id}",
            on_click=_reset_quiz_attempt,
            args=(quiz_id, len(quiz_set.get("questions", []))),
        )

    if submit:
        results = _grade_quiz(quiz_set, responses)
        st.session_state["study_quiz_results"][quiz_id] = results

    if not results:
        info_box("Answer the questions and use Check Answers to see your score and explanations.", title="Ready When You Are")
        return

    summary = f"You answered {results['answered']} of {results['total']} questions and scored {results['score']}."
    if results["score"] == results["total"]:
        success_box(summary, title="Excellent Result")
    elif results["score"] >= max(1, results["total"] // 2):
        info_box(summary, title="Quiz Complete")
    else:
        warning_box(summary, title="Keep Practicing")

    if results["answered"] < results["total"]:
        warning_box("Some questions were left unanswered. They are counted separately so you can review them and try again.", title="Incomplete Attempt")

    for detail in results["details"]:
        status = ":material/check_circle:" if detail["is_correct"] else ":material/error:"
        with st.expander(f"{status} Question {detail['number']}"):
            st.markdown(f"**Prompt:** {detail['prompt']}")
            st.markdown(f"**Your answer:** {detail['selected']}")
            st.markdown(f"**Correct answer:** {detail['correct']}")
            if detail["explanation"]:
                info_box(detail["explanation"], title="Why This Answer Is Correct")


def _flip_flashcard(deck_id: str) -> None:
    faces = st.session_state["study_flashcard_face"]
    faces[deck_id] = not faces.get(deck_id, False)


def _move_flashcard(deck_id: str, total_cards: int, direction: int) -> None:
    indices = st.session_state["study_flashcard_index"]
    current = indices.get(deck_id, 0)
    indices[deck_id] = (current + direction) % total_cards
    st.session_state["study_flashcard_face"][deck_id] = False


def _shuffle_flashcards(deck_id: str, total_cards: int) -> None:
    st.session_state["study_flashcard_index"][deck_id] = random.randrange(total_cards)
    st.session_state["study_flashcard_face"][deck_id] = False


def _render_flashcard_player(context: dict) -> None:
    deck = context.get("selected_deck")
    if not deck:
        return

    deck_id = deck["id"]
    cards = deck.get("cards", [])
    total_cards = len(cards)
    indices = st.session_state["study_flashcard_index"]
    faces = st.session_state["study_flashcard_face"]

    indices.setdefault(deck_id, 0)
    faces.setdefault(deck_id, False)

    current_index = indices[deck_id]
    showing_back = faces[deck_id]
    current_card = cards[current_index]

    st.markdown(
        f"""
<div class="crypto-card">
  <div style="font-size:18px;font-weight:700;margin-bottom:6px;">{deck["title"]}</div>
  <div style="color:var(--text-muted);font-size:14px;line-height:1.65;">{deck.get("description", "")}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    face_label = "Answer" if showing_back else "Prompt"
    face_value = current_card["back"] if showing_back else current_card["front"]
    st.markdown(
        f"""
<div class="crypto-card feature-card-blue" style="min-height:200px;">
  <div style="display:flex;justify-content:space-between;gap:16px;margin-bottom:14px;">
    <div style="font-size:13px;font-weight:700;color:var(--text-muted);text-transform:uppercase;">{face_label}</div>
    <div style="font-size:13px;color:var(--text-muted);">Card {current_index + 1} of {total_cards}</div>
  </div>
  <div style="font-size:1.1rem;font-weight:700;line-height:1.6;">{face_value}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    col_prev, col_flip, col_next, col_shuffle = st.columns(4)
    with col_prev:
        st.button(
            ":material/chevron_left: Previous",
            key=f"study_prev_{deck_id}",
            on_click=_move_flashcard,
            args=(deck_id, total_cards, -1),
        )
    with col_flip:
        st.button(
            ":material/autorenew: Flip",
            key=f"study_flip_{deck_id}",
            type="primary",
            on_click=_flip_flashcard,
            args=(deck_id,),
        )
    with col_next:
        st.button(
            ":material/chevron_right: Next",
            key=f"study_next_{deck_id}",
            on_click=_move_flashcard,
            args=(deck_id, total_cards, 1),
        )
    with col_shuffle:
        st.button(
            ":material/shuffle: Shuffle",
            key=f"study_shuffle_{deck_id}",
            on_click=_shuffle_flashcards,
            args=(deck_id, total_cards),
        )


def _build_context(quizzes: dict, flashcards: dict) -> dict:
    quiz_sets = quizzes.get("quiz_sets", [])
    decks = flashcards.get("decks", [])
    return {
        "quiz_sets": quiz_sets,
        "decks": decks,
        "quiz_set_count": len(quiz_sets),
        "quiz_question_count": sum(len(quiz_set.get("questions", [])) for quiz_set in quiz_sets),
        "quiz_topic_count": len({quiz_set.get("topic") for quiz_set in quiz_sets if quiz_set.get("topic")}),
        "deck_count": len(decks),
        "flashcard_count": sum(len(deck.get("cards", [])) for deck in decks),
        "flashcard_topic_count": len({deck.get("topic") for deck in decks if deck.get("topic")}),
        "filtered_count": 0,
    }


def _render_schema_view(view: dict, quizzes: dict, flashcards: dict) -> None:
    context = _build_context(quizzes, flashcards)
    view_id = view.get("id", "study")

    for component in view.get("components", []):
        comp_type = component.get("type")
        if comp_type == "hero_card":
            _render_hero_card(component)
        elif comp_type == "metric_strip":
            _render_metric_strip(component, context)
        elif comp_type == "topic_filter":
            _render_topic_filter(component, context, view_id)
        elif comp_type == "difficulty_filter":
            _render_difficulty_filter(component, context, view_id)
        elif comp_type == "dataset_selector":
            _render_dataset_selector(component, context, view_id)
        elif comp_type == "selection_summary":
            _render_selection_summary(component, context)
        elif comp_type == "quiz_player":
            _render_quiz_player(context)
        elif comp_type == "flashcard_player":
            _render_flashcard_player(context)


def render() -> None:
    render_brand_header(
        "Study Mode",
        "Review cryptography concepts with quiz practice and flashcard decks powered by JSON content.",
        compact=True,
    )

    _ensure_state()

    schema = load_study_schema()
    quizzes = load_study_quizzes()
    flashcards = load_study_flashcards()

    schema_ok, schema_msg = validate_study_schema(schema)
    if not schema_ok:
        error_box(schema_msg, title="Study Schema Problem")
        return

    quiz_ok, quiz_msg = validate_quiz_content(quizzes)
    if not quiz_ok:
        error_box(quiz_msg, title="Quiz Content Problem")
        return

    flashcard_ok, flashcard_msg = validate_flashcard_content(flashcards)
    if not flashcard_ok:
        error_box(flashcard_msg, title="Flashcard Content Problem")
        return

    info_box(
        "Study Mode keeps content in JSON so quiz sets, flashcard decks, and layout rules can be expanded without rewriting the page structure.",
        title="Schema-Driven Learning",
    )

    view_defs = schema.get("views", [])
    view_tabs = st.tabs([f":material/{view.get('icon', 'menu_book')}: {view.get('label', 'Study')}" for view in view_defs])

    for tab, view in zip(view_tabs, view_defs):
        with tab:
            _render_schema_view(view, quizzes, flashcards)

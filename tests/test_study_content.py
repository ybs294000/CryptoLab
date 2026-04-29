from __future__ import annotations

import unittest

from core.study_content import (
    load_study_flashcards,
    load_study_quizzes,
    load_study_schema,
    validate_flashcard_content,
    validate_quiz_content,
    validate_study_schema,
)


class StudyContentTests(unittest.TestCase):
    def test_study_schema_is_valid(self) -> None:
        schema = load_study_schema()
        ok, msg = validate_study_schema(schema)
        self.assertTrue(ok, msg)
        self.assertGreaterEqual(len(schema.get("views", [])), 2)

    def test_quiz_content_is_valid(self) -> None:
        quizzes = load_study_quizzes()
        ok, msg = validate_quiz_content(quizzes)
        self.assertTrue(ok, msg)
        self.assertGreaterEqual(len(quizzes.get("quiz_sets", [])), 3)

    def test_flashcard_content_is_valid(self) -> None:
        flashcards = load_study_flashcards()
        ok, msg = validate_flashcard_content(flashcards)
        self.assertTrue(ok, msg)
        self.assertGreaterEqual(len(flashcards.get("decks", [])), 2)


if __name__ == "__main__":
    unittest.main()

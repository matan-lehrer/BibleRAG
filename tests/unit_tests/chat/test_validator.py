import pytest

from chat.prompts import INSUFFICIENT_CONTEXT_MESSAGE, SOURCES_HEADER
from chat.validator import is_insufficient_context, validate_answer
from exception import AnswerValidationError


def test_substantive_answer_with_sources_passes():
    answer = f"אברהם הלך אל הארץ.\n\n{SOURCES_HEADER}\n- בראשית 12:1-6"
    assert validate_answer(answer) == answer.strip()


def test_insufficient_context_reply_is_exempt_from_sources():
    assert validate_answer(INSUFFICIENT_CONTEXT_MESSAGE) == INSUFFICIENT_CONTEXT_MESSAGE
    assert is_insufficient_context(INSUFFICIENT_CONTEXT_MESSAGE)


def test_empty_answer_rejected():
    with pytest.raises(AnswerValidationError):
        validate_answer("   ")


def test_substantive_answer_without_sources_rejected():
    with pytest.raises(AnswerValidationError):
        validate_answer("אברהם הלך אל הארץ.")

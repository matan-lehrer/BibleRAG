from chat.prompts import INSUFFICIENT_CONTEXT_MESSAGE, SOURCES_HEADER
from exception import AnswerValidationError


def is_insufficient_context(answer: str) -> bool:
    return INSUFFICIENT_CONTEXT_MESSAGE in answer


def validate_answer(answer: str) -> str:

    stripped = answer.strip()
    if not stripped:
        raise AnswerValidationError(details="Answer is empty.")

    if is_insufficient_context(stripped):
        return INSUFFICIENT_CONTEXT_MESSAGE

    if SOURCES_HEADER not in stripped:
        raise AnswerValidationError(details="Substantive answer is missing source references.")

    return stripped

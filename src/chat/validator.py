import logging

from chat.prompts import INSUFFICIENT_CONTEXT_MESSAGE, SOURCES_HEADER
from exception import AnswerValidationError

logger = logging.getLogger(__name__)


def is_insufficient_context(answer: str) -> bool:
    return INSUFFICIENT_CONTEXT_MESSAGE in answer


def validate_answer(answer: str) -> str:

    stripped = answer.strip()
    if not stripped:
        logger.warning("Validation failed: empty answer")
        raise AnswerValidationError(details="Answer is empty.")

    if is_insufficient_context(stripped):
        logger.warning("Answer reported insufficient context")
        return INSUFFICIENT_CONTEXT_MESSAGE

    if SOURCES_HEADER not in stripped:
        logger.warning("Validation failed: missing source references")
        raise AnswerValidationError(details="Substantive answer is missing source references.")

    return stripped

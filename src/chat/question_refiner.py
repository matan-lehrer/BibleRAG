import logging

from openai import OpenAI, OpenAIError

from chat.conversation_history import ConversationTurn
from chat.prompts import REFINER_SYSTEM_PROMPT
from consts import ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER
from exception import ConfigurationError
from settings import settings

Message = dict[str, str]

logger = logging.getLogger(__name__)


class QuestionRefiner:

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ConfigurationError(details="OPENAI_API_KEY is not configured.")
        if not settings.OPENAI_CHAT_MODEL:
            raise ConfigurationError(details="OPENAI_CHAT_MODEL is not configured.")
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_CHAT_MODEL

    def refine(self, question: str, history: list[ConversationTurn]) -> str:
        if not history:
            return question

        messages: list[Message] = [{"role": ROLE_SYSTEM, "content": REFINER_SYSTEM_PROMPT}]
        for turn in history:
            messages.append({"role": ROLE_USER, "content": turn.user_message})
            messages.append({"role": ROLE_ASSISTANT, "content": turn.assistant_message})
        messages.append({"role": ROLE_USER, "content": question})

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )
        except OpenAIError:
            logger.warning("Query refinement failed, using original question")
            return question

        refined = response.choices[0].message.content
        if not refined or not refined.strip():
            return question
        refined = refined.strip()
        logger.debug("Query refinement changed query: %s", refined != question.strip())
        return refined

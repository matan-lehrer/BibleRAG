from openai import OpenAI, OpenAIError

from exception import AnswerGenerationError, ConfigurationError
from settings import settings

Message = dict[str, str]


class AnswerGenerator:

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise ConfigurationError(details="OPENAI_API_KEY is not configured.")
        if not settings.OPENAI_CHAT_MODEL:
            raise ConfigurationError(details="OPENAI_CHAT_MODEL is not configured.")
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_CHAT_MODEL

    def generate(self, messages: list[Message]) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=0,
            )
        except OpenAIError as error:
            raise AnswerGenerationError(details=str(error)) from error

        content = response.choices[0].message.content
        if not content or not content.strip():
            raise AnswerGenerationError(details="Chat model returned an empty response.")
        return content.strip()

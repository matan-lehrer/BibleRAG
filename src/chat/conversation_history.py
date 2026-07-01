from collections import deque
from dataclasses import dataclass, field

from settings import settings


@dataclass
class ConversationTurn:
    user_message: str
    assistant_message: str


@dataclass
class ConversationHistory:
    _turns: deque[ConversationTurn] = field(
        default_factory=lambda: deque(maxlen=settings.CONVERSATION_MAX_TURNS)
    )

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        self._turns.append(ConversationTurn(user_message, assistant_message))

    def recent_turns(self) -> list[ConversationTurn]:
        return list(self._turns)

    def clear(self) -> None:
        self._turns.clear()

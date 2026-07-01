from collections import deque
from dataclasses import dataclass, field


@dataclass
class ConversationTurn:
    user_message: str
    assistant_message: str


@dataclass
class ConversationHistory:
    _turns: deque[ConversationTurn] = field(default_factory=deque)

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        raise NotImplementedError

    def recent_turns(self) -> list[ConversationTurn]:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

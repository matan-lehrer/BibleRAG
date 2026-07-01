from collections import deque

from chat.conversation_history import ConversationHistory, ConversationTurn
from chat.prompts import SOURCES_HEADER
from chat.retriever import RetrievedChunk
from chat.service import BibleChatService

Message = dict[str:str]


class _FakeRetriever:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def retrieve(self, question: str) -> list[RetrievedChunk]:
        self.questions.append(question)
        return [
            RetrievedChunk(
                text="וילך אברם",
                reference="בראשית 12:1-6",
                book="בראשית",
                chapter=12,
                start_verse=1,
                end_verse=6,
            )
        ]


class _FakeGenerator:
    def __init__(self) -> None:
        self.seen_messages: list[list[Message]] = []

    def generate(self, messages: list[Message]) -> str:
        self.seen_messages.append(messages)
        return f"אברם הלך.\n\n{SOURCES_HEADER}\n- בראשית 12:1-6"


class _FakeRefiner:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[ConversationTurn]]] = []

    def refine(self, question: str, history: list[ConversationTurn]) -> str:
        self.calls.append((question, history))
        return question


def _service() -> tuple[BibleChatService, _FakeRetriever, _FakeGenerator]:
    retriever, generator = _FakeRetriever(), _FakeGenerator()
    service = BibleChatService(
        retriever=retriever,
        generator=generator,
        history=ConversationHistory(deque(maxlen=5)),
        refiner=_FakeRefiner(),
    )
    return service, retriever, generator


def test_ask_returns_validated_answer_and_saves_turn():
    service, retriever, generator = _service()
    answer = service.ask("מי הלך?")

    assert SOURCES_HEADER in answer
    assert retriever.questions == ["מי הלך?"]
    service.ask("ולאן?")
    second_prompt = generator.seen_messages[1]
    assert any("מי הלך?" == m["content"] for m in second_prompt)


def test_reset_clears_history():
    service, _, generator = _service()
    service.ask("מי הלך?")
    service.reset()
    service.ask("שאלה חדשה")
    user_turns = [m for m in generator.seen_messages[-1] if m["role"] == "user"]
    assert len(user_turns) == 1

from chat.answer_generator import AnswerGenerator
from chat.conversation_history import ConversationHistory
from chat.question_refiner import QuestionRefiner
from chat.retriever import BibleRetriever


class BibleChatService:

    def __init__(
        self,
        retriever: BibleRetriever | None = None,
        generator: AnswerGenerator | None = None,
        history: ConversationHistory | None = None,
        refiner: QuestionRefiner | None = None,
    ) -> None:
        raise NotImplementedError

    def ask(self, question: str) -> str:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

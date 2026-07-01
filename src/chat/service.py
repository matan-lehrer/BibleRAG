from chat.answer_generator import AnswerGenerator
from chat.conversation_history import ConversationHistory
from chat.prompt_builder import build_messages
from chat.question_refiner import QuestionRefiner
from chat.retriever import BibleRetriever
from chat.validator import validate_answer


class BibleChatService:

    def __init__(
        self,
        retriever: BibleRetriever | None = None,
        generator: AnswerGenerator | None = None,
        history: ConversationHistory | None = None,
        refiner: QuestionRefiner | None = None,
    ) -> None:
        self._retriever = retriever or BibleRetriever()
        self._generator = generator or AnswerGenerator()
        self._history = history or ConversationHistory()
        self._refiner = refiner or QuestionRefiner()

    def ask(self, question: str) -> str:
        history = self._history.recent_turns()
        query = self._refiner.refine(question, history) if history else question
        chunks = self._retriever.retrieve(query)
        messages = build_messages(question, chunks, history)
        answer = self._generator.generate(messages)
        answer = validate_answer(answer)
        self._history.add_turn(question, answer)
        return answer

    def reset(self) -> None:
        self._history.clear()

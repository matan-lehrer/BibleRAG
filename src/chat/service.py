import logging

from chat.answer_generator import AnswerGenerator
from chat.conversation_history import ConversationHistory
from chat.prompt_builder import build_messages
from chat.question_refiner import QuestionRefiner
from chat.retriever import BibleRetriever
from chat.validator import validate_answer

logger = logging.getLogger(__name__)


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
        logger.info("Handling question (chars=%d)", len(question))
        history = self._history.recent_turns()
        logger.debug("Loaded %d history turns", len(history))
        query = self._refiner.refine(question, history) if history else question
        chunks = self._retriever.retrieve(query)
        messages = build_messages(question, chunks, history)
        answer = self._generator.generate(messages)
        answer = validate_answer(answer)
        self._history.add_turn(question, answer)
        logger.info("Answer ready (chars=%d, context_chunks=%d)", len(answer), len(chunks))
        return answer

    def reset(self) -> None:
        self._history.clear()

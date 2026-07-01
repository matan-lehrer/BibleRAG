from chat.conversation_history import ConversationTurn

Message = dict[str, str]


class QuestionRefiner:

    def __init__(self) -> None:
        raise NotImplementedError

    def refine(self, question: str, history: list[ConversationTurn]) -> str:
        raise NotImplementedError

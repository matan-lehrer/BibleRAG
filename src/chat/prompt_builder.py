from chat.conversation_history import ConversationTurn
from chat.retriever import RetrievedChunk

Message = dict[str, str]


def build_messages(
    question: str,
    chunks: list[RetrievedChunk],
    history: list[ConversationTurn],
) -> list[Message]:
    raise NotImplementedError

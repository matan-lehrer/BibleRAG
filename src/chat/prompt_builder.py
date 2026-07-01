from chat.conversation_history import ConversationTurn
from chat.prompts import (
    CONTEXT_HEADER,
    NO_RELEVANT_CHUNKS_MESSAGE,
    QUESTION_HEADER,
    SYSTEM_PROMPT,
)
from chat.retriever import RetrievedChunk
from consts import ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER

Message = dict[str, str]


def _format_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return NO_RELEVANT_CHUNKS_MESSAGE
    blocks = [f"[{chunk.reference}]\n{chunk.text}" for chunk in chunks]
    return "\n\n".join(blocks)


def _format_user_turn(question: str, chunks: list[RetrievedChunk]) -> str:
    return (
        f"{CONTEXT_HEADER}\n"
        f"{_format_context(chunks)}\n\n"
        f"{QUESTION_HEADER}{question.strip()}"
    )


def build_messages(
    question: str,
    chunks: list[RetrievedChunk],
    history: list[ConversationTurn],
) -> list[Message]:
    messages: list[Message] = [{"role": ROLE_SYSTEM, "content": SYSTEM_PROMPT}]
    for turn in history:
        messages.append({"role": ROLE_USER, "content": turn.user_message})
        messages.append({"role": ROLE_ASSISTANT, "content": turn.assistant_message})
    messages.append({"role": ROLE_USER, "content": _format_user_turn(question, chunks)})
    return messages

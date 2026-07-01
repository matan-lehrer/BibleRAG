from chat.conversation_history import ConversationTurn
from chat.prompt_builder import build_messages
from chat.prompts import SYSTEM_PROMPT
from chat.retriever import RetrievedChunk
from consts import ROLE_ASSISTANT, ROLE_SYSTEM, ROLE_USER


def _chunk(reference: str, text: str) -> RetrievedChunk:
    return RetrievedChunk(
        text=text,
        reference=reference,
        book="בראשית",
        chapter=12,
        start_verse=1,
        end_verse=6,
    )


def test_first_message_is_grounding_system_prompt():
    messages = build_messages("מי הלך?", [_chunk("בראשית 12:1-6", "וילך אברם")], [])
    assert messages[0] == {"role": ROLE_SYSTEM, "content": SYSTEM_PROMPT}


def test_context_and_question_are_in_final_user_turn():
    chunk = _chunk("בראשית 12:1-6", "וילך אברם כאשר דבר אליו יהוה")
    messages = build_messages("מי הלך?", [chunk], [])

    last = messages[-1]
    assert last["role"] == ROLE_USER
    assert chunk.text in last["content"]
    assert chunk.reference in last["content"]
    assert "מי הלך?" in last["content"]


def test_history_is_replayed_as_alternating_turns():
    history = [
        ConversationTurn("מי זה אברהם?", "אברהם הוא דמות במקרא. מקורות:\n- בראשית 12:1-6"),
    ]
    messages = build_messages("ומה לגבי שרה?", [_chunk("בראשית 12:1-6", "ושרי אשתו")], history)

    roles = [m["role"] for m in messages]
    assert roles == [ROLE_SYSTEM, ROLE_USER, ROLE_ASSISTANT, ROLE_USER]
    assert messages[1]["content"] == "מי זה אברהם?"
    assert messages[2]["content"].startswith("אברהם הוא דמות")


def test_no_context_yields_placeholder_so_model_reports_insufficient():
    messages = build_messages("שאלה ללא הקשר", [], [])
    assert "לא נמצאו קטעים רלוונטיים" in messages[-1]["content"]

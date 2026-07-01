from collections import deque

from chat.conversation_history import ConversationHistory, ConversationTurn


def _history(max_turns: int) -> ConversationHistory:
    return ConversationHistory(deque(maxlen=max_turns))


def test_keeps_only_last_max_turns():
    history = _history(max_turns=2)
    history.add_turn("q1", "a1")
    history.add_turn("q2", "a2")
    history.add_turn("q3", "a3")

    turns = history.recent_turns()
    assert len(turns) == 2
    assert turns[0] == ConversationTurn("q2", "a2")
    assert turns[-1] == ConversationTurn("q3", "a3")


def test_order_is_oldest_to_newest():
    history = _history(max_turns=5)
    history.add_turn("q1", "a1")
    history.add_turn("q2", "a2")

    assert [t.user_message for t in history.recent_turns()] == ["q1", "q2"]


def test_clear_empties_history():
    history = _history(max_turns=5)
    history.add_turn("q", "a")
    history.clear()
    assert len(history) == 0
    assert history.recent_turns() == []


def test_recent_turns_returns_a_copy():
    history = _history(max_turns=5)
    history.add_turn("q", "a")
    history.recent_turns().clear()
    assert len(history) == 1

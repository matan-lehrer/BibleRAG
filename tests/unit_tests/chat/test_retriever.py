import pytest
from langchain_core.documents import Document

from chat import retriever as retriever_module
from chat.retriever import BibleRetriever, RetrievedChunk
from exception import RetrievalError


def _document(reference: str, text: str) -> Document:
    book, rest = reference.split(" ", 1)
    chapter, verses = rest.split(":", 1)
    start, _, end = verses.partition("-")
    return Document(
        page_content=text,
        metadata={
            "book": book,
            "chapter": int(chapter),
            "start_verse": int(start),
            "end_verse": int(end or start),
            "reference": reference,
        },
    )


class _FakeStore:
    """Stand-in for Chroma that records the query and returns canned documents."""

    def __init__(self, documents: list[Document]) -> None:
        self._documents = documents
        self.calls: list[tuple[str, int]] = []

    def similarity_search(self, query: str, k: int) -> list[Document]:
        self.calls.append((query, k))
        return self._documents[:k]


@pytest.fixture
def patched_retriever(monkeypatch):
    """A BibleRetriever whose backing store is a fake, so no OpenAI/Chroma is touched."""
    documents = [
        _document("בראשית 12:1-6", "וילך אברם"),
        _document("בראשית 15:1-5", "אחר הדברים האלה"),
    ]
    store = _FakeStore(documents)

    monkeypatch.setattr(BibleRetriever, "__init__", lambda self, top_k=None: None)
    retriever = BibleRetriever()
    retriever._store = store
    retriever._top_k = 6
    return retriever, store


def test_maps_documents_to_retrieved_chunks(patched_retriever):
    retriever, _ = patched_retriever
    chunks = retriever.retrieve("מי הלך?")

    assert all(isinstance(c, RetrievedChunk) for c in chunks)
    assert chunks[0].reference == "בראשית 12:1-6"
    assert chunks[0].book == "בראשית"
    assert chunks[0].start_verse == 1
    assert chunks[0].end_verse == 6


def test_top_k_override_is_passed_through(patched_retriever):
    retriever, store = patched_retriever
    chunks = retriever.retrieve("מי הלך?", top_k=1)

    assert len(chunks) == 1
    assert store.calls == [("מי הלך?", 1)]


def test_empty_question_rejected(patched_retriever):
    retriever, _ = patched_retriever
    with pytest.raises(RetrievalError):
        retriever.retrieve("   ")


def test_missing_metadata_raises_retrieval_error():
    bad = Document(page_content="text", metadata={"book": "בראשית"})
    with pytest.raises(RetrievalError):
        RetrievedChunk.from_document(bad)


def test_store_failure_is_wrapped(patched_retriever, monkeypatch):
    retriever, store = patched_retriever

    def _boom(query, k):
        raise RuntimeError("chroma down")

    monkeypatch.setattr(store, "similarity_search", _boom)
    with pytest.raises(RetrievalError):
        retriever.retrieve("מי הלך?")

    assert retriever_module.RetrievalError is RetrievalError

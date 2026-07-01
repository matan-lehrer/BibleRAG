import pytest
from langchain_chroma import Chroma
from langchain_core.embeddings.fake import DeterministicFakeEmbedding

from indexing import vector_store
from models.bible_chunk import BibleChunk
from models.verse import Verse
from settings import settings

EMBED_SIZE = 16


def _verse(book: str, chapter: int, verse: int, text: str) -> Verse:
    return Verse(book=book, chapter=chapter, verse=verse, text=text)


@pytest.fixture
def indexed_store(monkeypatch, tmp_path):
    chunks = [
        BibleChunk(
            [_verse("בראשית", 1, 1, "בראשית ברא אלהים"), _verse("בראשית", 1, 2, "והארץ היתה תהו")]
        ),
        BibleChunk(
            [
                _verse("בראשית", 1, 3, "ויאמר אלהים יהי אור"),
                _verse("בראשית", 1, 4, "וירא אלהים את האור"),
            ]
        ),
        BibleChunk([_verse("שמות", 2, 1, "וילך איש מבית לוי")]),
        BibleChunk([_verse("שמות", 2, 2, "ותהר האשה ותלד בן")]),
        BibleChunk([_verse("שמות", 2, 3, "ולא יכלה עוד הצפינו")]),
        BibleChunk([_verse("שמות", 3, 1, "   ")]),  # whitespace-only -> must be filtered out
    ]
    nonempty = chunks[:-1]

    monkeypatch.setattr(
        vector_store, "_build_embeddings", lambda: DeterministicFakeEmbedding(size=EMBED_SIZE)
    )
    monkeypatch.setattr(settings, "CHROMA_PERSIST_DIR", tmp_path)
    monkeypatch.setattr(settings, "CHROMA_COLLECTION_NAME", "test_bible_chunks")
    monkeypatch.setattr(settings, "VECTOR_STORE_BATCH_SIZE", 2)
    monkeypatch.setattr(settings, "DEBUG_VECTOR_STORE", False)

    vector_store.build_vector_store(chunks, reset=True)

    store = Chroma(
        collection_name="test_bible_chunks",
        embedding_function=DeterministicFakeEmbedding(size=EMBED_SIZE),
        persist_directory=str(tmp_path),
    )
    return store, nonempty


def test_indexes_only_nonempty_chunks(indexed_store):
    store, nonempty = indexed_store
    assert store._collection.count() == len(nonempty)


def test_known_item_retrieval(indexed_store):
    store, nonempty = indexed_store
    target = nonempty[2]

    hits = store.similarity_search(target.text, k=1)

    assert len(hits) == 1
    hit = hits[0]
    assert hit.page_content == target.text
    assert hit.metadata["reference"] == "שמות 2:1"
    assert hit.metadata["book"] == "שמות"
    assert hit.metadata["chapter"] == 2
    assert hit.metadata["start_verse"] == 1
    assert hit.metadata["end_verse"] == 1


def test_multi_verse_reference_and_metadata(indexed_store):
    store, nonempty = indexed_store
    target = nonempty[0]  # בראשית 1:1-2

    hit = store.similarity_search(target.text, k=1)[0]

    assert hit.metadata["reference"] == "בראשית 1:1-2"
    assert hit.metadata["start_verse"] == 1
    assert hit.metadata["end_verse"] == 2


def test_all_hits_carry_full_metadata(indexed_store):
    store, _ = indexed_store
    hits = store.similarity_search("בראשית", k=5)
    for hit in hits:
        assert hit.metadata.keys() >= {
            "book",
            "chapter",
            "start_verse",
            "end_verse",
            "reference",
        }


def test_empty_chunks_raise():
    with pytest.raises(vector_store.VectorStoreError):
        vector_store.build_vector_store([])

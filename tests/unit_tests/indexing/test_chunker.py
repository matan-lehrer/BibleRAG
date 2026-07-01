import pytest

from exception import ChunkingError
from indexing.chunker import build_chunks
from models.verse import Verse


def _verse(book: str, chapter: int, verse: int) -> Verse:
    return Verse(book=book, chapter=chapter, verse=verse, text=f"{book} {chapter}:{verse}")


def _chapter(book: str, chapter: int, count: int) -> list[Verse]:
    return [_verse(book, chapter, v) for v in range(1, count + 1)]


def test_windows_respect_overlap_stride():
    verses = _chapter("בראשית", 1, 5)

    chunks = build_chunks(verses, window_size=3, overlap=1)

    assert [(c.start_verse, c.end_verse) for c in chunks] == [(1, 3), (3, 5)]


def test_last_chunk_may_be_shorter_than_window():
    verses = _chapter("בראשית", 1, 5)

    chunks = build_chunks(verses, window_size=3, overlap=0)

    assert [[v.verse for v in c.verses] for c in chunks] == [[1, 2, 3], [4, 5]]
    assert len(chunks[-1].verses) == 2


def test_never_crosses_book_or_chapter_boundaries():
    verses = [
        *_chapter("בראשית", 1, 2),
        *_chapter("בראשית", 2, 1),
        *_chapter("שמות", 1, 1),
    ]

    chunks = build_chunks(verses, window_size=5, overlap=0)

    assert [(c.book, c.chapter, c.start_verse, c.end_verse) for c in chunks] == [
        ("בראשית", 1, 1, 2),
        ("בראשית", 2, 1, 1),
        ("שמות", 1, 1, 1),
    ]


def test_single_verse_chapter_yields_one_chunk():
    verses = _chapter("עובדיה", 1, 1)

    chunks = build_chunks(verses, window_size=3, overlap=1)

    assert len(chunks) == 1
    assert chunks[0].start_verse == chunks[0].end_verse == 1


def test_empty_input_returns_no_chunks():
    assert build_chunks([], window_size=3, overlap=1) == []


@pytest.mark.parametrize(
    "window_size, overlap",
    [
        (0, 0), 
        (3, 3), 
        (3, 4), 
        (3, -1),
    ],
)
def test_invalid_config_raises(window_size: int, overlap: int):
    with pytest.raises(ChunkingError):
        build_chunks(_chapter("בראשית", 1, 3), window_size=window_size, overlap=overlap)

from itertools import groupby

from exception import ChunkingError
from models.bible_chunk import BibleChunk
from models.verse import Verse
from settings import settings

MIN_WINDOW_SIZE = 1


def build_chunks(
    verses: list[Verse],
    window_size: int = settings.CHUNK_WINDOW_SIZE,
    overlap: int = settings.CHUNK_OVERLAP,
) -> list[BibleChunk]:
    _validate_config(window_size, overlap)
    step = window_size - overlap
    chunks: list[BibleChunk] = []
    for _, chapter in groupby(verses, key=lambda verse: (verse.book, verse.chapter)):
        chapter_verses = list(chapter)
        for start in range(0, len(chapter_verses), step):
            chunks.append(BibleChunk(chapter_verses[start : start + window_size]))
            if start + window_size >= len(chapter_verses):
                break
    return chunks


def _validate_config(window_size: int, overlap: int) -> None:
    if window_size < MIN_WINDOW_SIZE:
        raise ChunkingError(f"window_size must be >= {MIN_WINDOW_SIZE}, got {window_size}.")
    if not 0 <= overlap < window_size:
        raise ChunkingError(f"overlap must satisfy 0 <= overlap < window_size, got {overlap}.")

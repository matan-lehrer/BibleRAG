from models.bible_chunk import BibleChunk
from models.verse import Verse


def build_chunks(
    verses: list[Verse],
    window_size: int = 6,
    overlap: int = 2,
) -> list[BibleChunk]:
    raise NotImplementedError

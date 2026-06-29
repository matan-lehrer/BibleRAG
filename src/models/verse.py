from dataclasses import dataclass


@dataclass
class Verse:
    book: str
    chapter: int
    verse: int
    raw_text: str
    clean_text: str

from dataclasses import dataclass


@dataclass
class Verse:
    book: str
    chapter: int
    verse: int
    text: str

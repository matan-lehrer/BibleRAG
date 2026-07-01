from dataclasses import dataclass

from models.verse import Verse


@dataclass
class BibleChunk:
    verses: list[Verse]

    @property
    def book(self):
        return self.verses[0].book

    @property
    def chapter(self):
        return self.verses[0].chapter

    @property
    def start_verse(self):
        return self.verses[0].verse

    @property
    def end_verse(self):
        return self.verses[-1].verse

    @property
    def text(self):
        return "\n".join(v.text for v in self.verses)

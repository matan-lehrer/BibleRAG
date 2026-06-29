from models.verse import Verse


class BibleParser:
    """
    Parses raw extracted Bible text into structured Verse objects.
    """

    def __init__(self, bible_text: str):
        self.raw_text = bible_text
        self.verses: list[Verse] = []

    def parse(self) -> list[Verse]:
        raise NotImplementedError

    def _parse_books(self):
        raise NotImplementedError

    def _parse_chapters(self):
        raise NotImplementedError

    def _parse_verses(self):
        raise NotImplementedError

import re

from indexing.hebrew_cleaner import SOF_PASUK, to_hebrew_words
from models.verse import Verse

CHAPTER_HEADER = re.compile(r"^\W*פרק\s+(?P<num>\S+?)\s*-\s*(?P<book>.+?)\s*$")

BOOK_HEADING = re.compile(r"^[א-ת ]+$")

_VERSE_MARKER = re.compile(r"'[א-ת]" r'|[א-ת]"[א-ת]' r'|"[א-ת]{2,3}' r'|[א-ת]{2,3}"')


class BibleParser:
    def __init__(self, bible_text: str):
        self.text = bible_text
        self.verses: list[Verse] = []

    def parse(self) -> list[Verse]:
        current_book: str | None = None
        current_chapter = 0
        chapter_lines: list[str] = []

        def flush_chapter() -> None:
            if current_book and current_chapter and chapter_lines:
                self._emit_chapter(" ".join(chapter_lines), current_book, current_chapter)
            chapter_lines.clear()

        for line in self.text.splitlines():
            if not line:
                continue

            header = CHAPTER_HEADER.match(line)
            if header is not None:
                flush_chapter()
                book = header.group("book")
                if book != current_book:
                    current_book = book
                    current_chapter = 0
                current_chapter += 1
                continue

            if BOOK_HEADING.match(line):
                continue

            chapter_lines.append(line)

        flush_chapter()
        return self.verses

    def _emit_chapter(self, chapter_body: str, book: str, chapter: int) -> None:
        verse_num = 0
        for piece in chapter_body.split(SOF_PASUK):
            text = to_hebrew_words(_VERSE_MARKER.sub(" ", piece))
            if not text:
                continue
            verse_num += 1
            self.verses.append(Verse(book=book, chapter=chapter, verse=verse_num, text=text))

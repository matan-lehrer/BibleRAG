import json
import re
from pathlib import Path

from indexing.hebrew_utils import clean_verse
from indexing.text_normalizer import normalize_line
from models.verse import Verse
from settings import settings

CHAPTER_HEADER = re.compile(r"^\W*פרק\s+(?P<num>\S+?)\s*-\s*(?P<book>.+?)\s*$")

BOOK_HEADING = re.compile(r"^[א-ת ]+$")

_SOF_PASUK = "׃"

_VERSE_MARKER = re.compile(r"'[א-ת]" r'|[א-ת]"[א-ת]' r'|"[א-ת]{2,3}' r'|[א-ת]{2,3}"')


class BibleParser:
    DEBUG_PATH = Path("data/debugging/verse.json")

    def __init__(self, bible_text: str):
        self.raw_text = bible_text
        self.verses: list[Verse] = []

    def parse(self) -> list[Verse]:
        current_book: str | None = None
        current_chapter = 0
        chapter_lines: list[str] = []

        def flush_chapter() -> None:
            if current_book and current_chapter and chapter_lines:
                self._emit_chapter(" ".join(chapter_lines), current_book, current_chapter)
            chapter_lines.clear()

        for raw_line in self.raw_text.splitlines():
            line = normalize_line(raw_line)
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

        if settings.DEBUG_PARSER:
            self._save_debug_output()

        return self.verses

    def _emit_chapter(self, chapter_raw: str, book: str, chapter: int) -> None:
        """Split a chapter body on sof-pasuk and emit each piece as a verse."""
        verse_num = 0
        for piece in chapter_raw.split(_SOF_PASUK):
            raw = _VERSE_MARKER.sub(" ", piece).strip()
            if not raw:
                continue
            verse_num += 1
            self._emit(book, chapter, verse_num, raw)

    def _emit(self, book: str, chapter: int, verse: int, raw: str) -> None:
        self.verses.append(
            Verse(
                book=book,
                chapter=chapter,
                verse=verse,
                raw_text=raw,
                clean_text=clean_verse(raw),
            )
        )

    def _save_debug_output(self) -> None:
        self.DEBUG_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = [
            {
                "book": v.book,
                "chapter": v.chapter,
                "verse": v.verse,
                "raw_text": v.raw_text,
                "clean_text": v.clean_text,
            }
            for v in self.verses
        ]
        self.DEBUG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

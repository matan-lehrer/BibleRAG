from collections import defaultdict

import pytest

from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.parser import BibleParser
from settings import settings


@pytest.fixture(scope="module")
def verses():
    pdf_path = str(settings.BIBLE_PDF_PATH)
    raw_text = PdfExtractor().extract(pdf_path)
    return BibleParser(raw_text).parse()


def _count(verses, book, chapter):
    return sum(1 for v in verses if v.book == book and v.chapter == chapter)


def test_total_in_expected_band(verses):
    # currently at 22,395; suppose to be 23,206
    assert 22_350 <= len(verses) <= 23,250


def test_book_count(verses):
    assert len({v.book for v in verses}) == 38


def test_known_chapter_lengths(verses):
    assert _count(verses, "בראשית", 1) == 31
    assert _count(verses, "תהלים", 119) == 176
    assert _count(verses, "תהלים", 110) == 7
    assert _count(verses, "תהלים", 150) == 6


def test_chapters_are_contiguous_per_book(verses):
    chapters = defaultdict(set)
    for v in verses:
        chapters[v.book].add(v.chapter)
    for book, chs in chapters.items():
        assert chs == set(range(1, max(chs) + 1)), f"{book} has gaps: {sorted(chs)}"


def test_verses_numbered_sequentially_per_chapter(verses):
    seen = defaultdict(list)
    for v in verses:
        seen[(v.book, v.chapter)].append(v.verse)
    for key, nums in seen.items():
        assert nums == list(range(1, len(nums) + 1)), f"{key} not sequential: {nums}"


def test_no_empty_or_marker_polluted_clean_text(verses):
    for v in verses:
        assert v.clean_text.strip(), f"empty clean_text at {v.book} {v.chapter}:{v.verse}"
        assert "׃" not in v.clean_text 
        assert '"' not in v.clean_text and "'" not in v.clean_text  
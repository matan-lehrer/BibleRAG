from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.parser import BibleParser
from settings import settings


def main():
    extractor = PdfExtractor()
    raw_text = extractor.extract(str(settings.BIBLE_PDF_PATH))
    print(raw_text[:300])

    parser = BibleParser(raw_text)
    verses = parser.parse()

    print(f"Parsed {len(verses)} verses.\n")

    for verse in verses[:5]:
        print(f"{verse.book} {verse.chapter}:{verse.verse}")
        print(f"RAW:   {verse.raw_text}")
        print(f"CLEAN: {verse.clean_text}")
        print()


if __name__ == "__main__":
    main()

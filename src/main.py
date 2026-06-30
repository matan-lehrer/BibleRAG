from indexing.chunker import build_chunks
from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.parser import BibleParser
from settings import settings


def main() -> None:
    extractor = PdfExtractor()
    raw_text = extractor.extract(str(settings.BIBLE_PDF_PATH))
    print(f"Extracted {len(raw_text)} characters.\n")

    verses = BibleParser(raw_text).parse()
    print(f"Parsed {len(verses)} verses.\n")

    chunks = build_chunks(verses)
    print(f"Built {len(chunks)} chunks.\n")


if __name__ == "__main__":
    main()

from indexing.chunker import build_chunks
from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.hebrew_cleaner import clean
from indexing.parser import BibleParser
from indexing.vector_store import build_vector_store
from settings import settings


def main() -> None:
    raw_text = PdfExtractor().extract(str(settings.BIBLE_PDF_PATH))
    cleaned = clean(raw_text)
    verses = BibleParser(cleaned).parse()
    chunks = build_chunks(verses)
    build_vector_store(chunks, reset=True)
    print(f"Indexed vectors into {settings.CHROMA_PERSIST_DIR}.")


if __name__ == "__main__":
    main()

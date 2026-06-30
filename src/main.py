from indexing.chunker import build_chunks
from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.parser import BibleParser
from indexing.vector_store import build_documents, build_vector_store
from settings import settings


def main() -> None:
    extractor = PdfExtractor()
    raw_text = extractor.extract(str(settings.BIBLE_PDF_PATH))

    verses = BibleParser(raw_text).parse()
    print(f"Parsed {len(verses)} verses.\n")

    chunks = build_chunks(verses)
    print(f"Built {len(chunks)} chunks.\n")

    documents = build_documents(chunks)
    print(f"Built {len(documents)} documents.\n")

    build_vector_store(chunks)
    print(f"Indexed vectors into {settings.CHROMA_PERSIST_DIR}.")


if __name__ == "__main__":
    main()

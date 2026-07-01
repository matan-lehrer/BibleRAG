import logging

from indexing.chunker import build_chunks
from indexing.extractors.pdf_extractor import PdfExtractor
from indexing.hebrew_cleaner import clean
from indexing.parser import BibleParser
from indexing.vector_store import build_vector_store
from logging_config import configure_logging
from settings import settings

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()
    logger.info("Starting indexing pipeline")
    try:
        raw_text = PdfExtractor().extract(str(settings.BIBLE_PDF_PATH))
        cleaned = clean(raw_text)
        logger.debug("Extracted %d chars, cleaned to %d chars", len(raw_text), len(cleaned))
        verses = BibleParser(cleaned).parse()
        logger.info("Parsed %d verses", len(verses))
        chunks = build_chunks(verses)
        logger.info("Built %d chunks", len(chunks))
        build_vector_store(chunks, reset=True)
        logger.info("Indexed vectors into %s", settings.CHROMA_PERSIST_DIR)
    except Exception:
        logger.exception("Indexing pipeline failed")
        raise


if __name__ == "__main__":
    main()

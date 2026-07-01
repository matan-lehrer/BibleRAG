from pathlib import Path

import fitz

from consts import PDF_EXTENSION
from exception import DocumentExtractionError, UnsupportedFileTypeError
from indexing.extractors.base import DocumentExtractor


class PdfExtractor(DocumentExtractor):
    def extract(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise DocumentExtractionError(file_path)

        if path.suffix.lower() != PDF_EXTENSION:
            raise UnsupportedFileTypeError(path.suffix)

        pages: list[str] = []

        flags = fitz.TEXTFLAGS_TEXT | fitz.TEXT_INHIBIT_SPACES

        with fitz.open(path) as pdf:
            for page in pdf:
                pages.append(page.get_text("text", flags=flags))

        return "\n".join(pages).strip()

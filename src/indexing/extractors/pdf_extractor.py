from indexing.extractors.base import DocumentExtractor


class PdfExtractor(DocumentExtractor):
    def extract(self, file_path: str) -> str:
        raise NotImplementedError

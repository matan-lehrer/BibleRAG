from indexing.extractors.pdf_extractor import PdfExtractor
from settings import settings


def main():
    extractor = PdfExtractor()
    text = extractor.extract(str(settings.BIBLE_PDF_PATH))
    print(text[:300])


if __name__ == "__main__":
    main()

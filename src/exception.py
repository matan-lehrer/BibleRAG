class BibleRAGError(Exception):
    default_message = "An unexpected Bible RAG error occurred."

    def __init__(self, details: str | None = None):
        message = self.default_message
        if details:
            message = f"{message}: {details}"
        super().__init__(message)


class ConfigurationError(BibleRAGError):
    default_message = "Application configuration is invalid."


class DocumentExtractionError(BibleRAGError):
    default_message = "Failed to extract text from document."


class UnsupportedFileTypeError(BibleRAGError):
    default_message = "Unsupported document file type."


class BibleParsingError(BibleRAGError):
    default_message = "Failed to parse Bible text."


class ChunkingError(BibleRAGError):
    default_message = "Failed to build Bible chunks."


class VectorStoreError(BibleRAGError):
    default_message = "Vector store operation failed."


class RetrievalError(BibleRAGError):
    default_message = "Failed to retrieve context from the vector store."


class AnswerGenerationError(BibleRAGError):
    default_message = "Failed to generate an answer from the chat model."


class AnswerValidationError(BibleRAGError):
    default_message = "Generated answer failed validation."

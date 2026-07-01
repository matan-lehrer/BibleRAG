from __future__ import annotations

import logging
from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from exception import ConfigurationError, RetrievalError
from settings import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RetrievedChunk:

    text: str
    reference: str
    book: str
    chapter: int
    start_verse: int
    end_verse: int

    @classmethod
    def from_document(cls, document: Document) -> RetrievedChunk:
        metadata = document.metadata
        try:
            return cls(
                text=document.page_content,
                reference=metadata["reference"],
                book=metadata["book"],
                chapter=metadata["chapter"],
                start_verse=metadata["start_verse"],
                end_verse=metadata["end_verse"],
            )
        except KeyError as error:
            raise RetrievalError(details=f"Retrieved document missing metadata {error}.") from error


class BibleRetriever:

    def __init__(self, top_k: int | None = None) -> None:
        if not settings.OPENAI_API_KEY:
            raise ConfigurationError(details="OPENAI_API_KEY is not configured.")
        self._top_k = top_k if top_k is not None else settings.RETRIEVER_TOP_K
        self._store = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=OpenAIEmbeddings(
                model=settings.OPENAI_EMBEDDING_MODEL,
                api_key=settings.OPENAI_API_KEY,
            ),
            persist_directory=str(settings.CHROMA_PERSIST_DIR),
        )

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedChunk]:
        if not question.strip():
            raise RetrievalError(details="Question must not be empty.")
        k = top_k if top_k is not None else self._top_k
        try:
            documents = self._store.similarity_search(question, k=k)
        except Exception as error:
            logger.exception("Similarity search failed")
            raise RetrievalError(details=str(error)) from error

        if not documents:
            logger.warning("No chunks retrieved")
        elif len(documents) < k:
            logger.warning("Weak retrieval: %d of %d chunks", len(documents), k)

        chunks = [RetrievedChunk.from_document(document) for document in documents]
        logger.debug("Retrieved references: %s", [chunk.reference for chunk in chunks])
        return chunks

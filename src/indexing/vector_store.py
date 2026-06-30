import json
from collections.abc import Iterator, Sequence
from typing import TypeVar

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from exception import VectorStoreError
from models.bible_chunk import BibleChunk
from settings import settings

T = TypeVar("T")


def batched(items: Sequence[T], batch_size: int) -> Iterator[list[T]]:
    if batch_size <= 0:
        raise VectorStoreError(details=f"batch_size must be positive, got {batch_size}.")
    for start in range(0, len(items), batch_size):
        yield list(items[start : start + batch_size])


def _chunk_reference(chunk: BibleChunk) -> str:
    if chunk.start_verse == chunk.end_verse:
        return f"{chunk.book} {chunk.chapter}:{chunk.start_verse}"
    return f"{chunk.book} {chunk.chapter}:{chunk.start_verse}-{chunk.end_verse}"


def _chunk_id(chunk: BibleChunk) -> str:
    return f"{chunk.book}_{chunk.chapter}_{chunk.start_verse}_{chunk.end_verse}"


def chunk_to_document(chunk: BibleChunk) -> Document:
    return Document(
        page_content=chunk.text,
        metadata={
            "book": chunk.book,
            "chapter": chunk.chapter,
            "start_verse": chunk.start_verse,
            "end_verse": chunk.end_verse,
            "reference": _chunk_reference(chunk),
        },
    )


def _save_documents_debug_output(documents: list[Document]) -> None:
    settings.DOCUMENTS_DEBUG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in documents]
    settings.DOCUMENTS_DEBUG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def build_documents(chunks: list[BibleChunk]) -> list[Document]:
    documents = [chunk_to_document(chunk) for chunk in chunks]
    if settings.DEBUG_VECTOR_STORE:
        _save_documents_debug_output(documents)
    return documents


def _build_embeddings() -> OpenAIEmbeddings:
    if not settings.OPENAI_API_KEY:
        raise VectorStoreError(details="OPENAI_API_KEY is not configured.")
    return OpenAIEmbeddings(
        model=settings.OPENAI_EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )


def build_vector_store(chunks: list[BibleChunk], *, reset: bool = False) -> None:
    indexable = [chunk for chunk in chunks if chunk.text.strip()]
    if not indexable:
        raise VectorStoreError(details="No non-empty chunks to index.")

    documents = build_documents(indexable)
    ids = [_chunk_id(chunk) for chunk in indexable]

    store = Chroma(
        collection_name=settings.CHROMA_COLLECTION_NAME,
        embedding_function=_build_embeddings(),
        persist_directory=str(settings.CHROMA_PERSIST_DIR),
    )

    if reset:
        store.reset_collection()

    batch_size = settings.VECTOR_STORE_BATCH_SIZE
    for doc_batch, id_batch in zip(
        batched(documents, batch_size), batched(ids, batch_size), strict=True
    ):
        store.add_documents(documents=doc_batch, ids=id_batch)

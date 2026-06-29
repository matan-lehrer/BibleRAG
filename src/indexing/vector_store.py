from langchain_chroma import Chroma

from models.bible_chunk import BibleChunk


def build_vector_store(
    chunks: list[BibleChunk],
    persist_directory: str,
) -> Chroma:
    """
    Build a new Chroma vector database from BibleChunk objects.
    """
    raise NotImplementedError


def load_vector_store(
    persist_directory: str,
) -> Chroma:
    """
    Load an existing Chroma vector database.
    """
    raise NotImplementedError

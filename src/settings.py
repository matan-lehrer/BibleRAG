from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BIBLE_PDF_PATH: Path
    CHUNKS_DEBUG_PATH: Path
    DOCUMENTS_DEBUG_PATH: Path
    CHROMA_PERSIST_DIR: Path

    DEBUG_PARSER: bool
    DEBUG_VECTOR_STORE: bool
    CHUNK_WINDOW_SIZE: int
    CHUNK_OVERLAP: int

    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str
    CHROMA_COLLECTION_NAME: str
    VECTOR_STORE_BATCH_SIZE: int

    OPENAI_CHAT_MODEL: str
    RETRIEVER_TOP_K: int
    CONVERSATION_MAX_TURNS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

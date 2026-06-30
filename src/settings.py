from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BIBLE_PDF_PATH: Path
    CHUNKS_DEBUG_PATH: Path
    DEBUG_PARSER: bool = False

    CHUNK_WINDOW_SIZE: int = 6
    CHUNK_OVERLAP: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

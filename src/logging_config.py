import logging
from pathlib import Path

from settings import settings

_NOISY_LOGGERS = ("httpx", "httpcore", "openai", "urllib3", "chromadb")
_DEFAULT_LOG_FILE = Path("./data/logs/bible_rag.log")


def configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(settings.LOG_LEVEL.upper())

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    # Logs are written to a file only, never to the terminal, so normal runs
    # stay clean. Set LOG_FILE_PATH in .env to override the destination.
    log_file = settings.LOG_FILE_PATH or _DEFAULT_LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

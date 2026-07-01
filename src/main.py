from chat.cli import run_cli
from chat.service import BibleChatService
from logging_config import configure_logging


def main() -> None:
    configure_logging()
    service = BibleChatService()
    run_cli(service)


if __name__ == "__main__":
    main()

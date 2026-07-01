from chat.cli import run_cli
from chat.service import BibleChatService


def main() -> None:
    service = BibleChatService()
    run_cli(service)


if __name__ == "__main__":
    main()

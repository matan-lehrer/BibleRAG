from chat.service import BibleChatService
from consts import (
    CLI_BANNER,
    CLI_ERROR,
    CLI_GOODBYE,
    CLI_HISTORY_CLEARED,
    EXIT_COMMANDS,
    RESET_COMMANDS,
)
from exception import BibleRAGError


def run_cli(service: BibleChatService) -> None:
    print(f"{CLI_BANNER}\n")
    while True:
        try:
            question = input("> ").strip()

            if not question:
                continue
            command = question.lower()
            if command in EXIT_COMMANDS:
                print(CLI_GOODBYE)
                break
            if command in RESET_COMMANDS:
                service.reset()
                print(f"{CLI_HISTORY_CLEARED}\n")
                continue

            try:
                answer = service.ask(question)
                print(f"\n{answer}\n")
            except BibleRAGError as error:
                print(f"\n{CLI_ERROR}\n({error})\n")

        except (EOFError, KeyboardInterrupt):
            print(f"\n{CLI_GOODBYE}")
            break

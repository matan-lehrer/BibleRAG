Message = dict[str, str]


class AnswerGenerator:

    def __init__(self) -> None:
        raise NotImplementedError

    def generate(self, messages: list[Message]) -> str:
        raise NotImplementedError

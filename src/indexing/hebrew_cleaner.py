import re

SOF_PASUK = "׃"

_SECTION_MARKER = re.compile(r"[{}]\s*[פס]?")

_MAQAF = re.compile("־")

_NIKUD_TEAMIM = re.compile("[֑-ׂׄ-ׇ]")

_WHITESPACE = re.compile(r"\s+")

_NON_HEBREW = re.compile(r"[^א-ת ]")


def clean(text: str) -> str:
    return "\n".join(_clean_line(line) for line in text.splitlines())


def _clean_line(line: str) -> str:
    line = _SECTION_MARKER.sub(" ", line)
    line = _MAQAF.sub(" ", line)
    line = _NIKUD_TEAMIM.sub("", line)
    return _WHITESPACE.sub(" ", line).strip()


def to_hebrew_words(text: str) -> str:
    return re.sub(r" +", " ", _NON_HEBREW.sub("", text)).strip()

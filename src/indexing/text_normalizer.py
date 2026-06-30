import re

_PARAGRAPH_MARKER = re.compile(r"\}\{[א-ת]?")

_PASEQ = re.compile(r"׀")

_LAYOUT_SPACE = re.compile(r"[\xa0 ]")

_MULTISPACE = re.compile(r" +")


def normalize_line(line: str) -> str:
    line = _PARAGRAPH_MARKER.sub(" ", line)
    line = _PASEQ.sub(" ", line)
    line = _LAYOUT_SPACE.sub(" ", line)
    return _MULTISPACE.sub(" ", line).strip()

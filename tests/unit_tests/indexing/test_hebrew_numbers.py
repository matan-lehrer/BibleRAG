import pytest

from indexing.hebrew_utils import parse_hebrew_numeral


@pytest.mark.parametrize(
    "numeral, expected",
    [
        ("א", 1),
        ("י", 10),
        ('י"א', 11),
        ('ט"ו', 15),
        ('א"ו', 106),
        ("איא", 111),
        ("אלא", 131),
        ("אעו", 176),
        ("ק", 100),
        ("קנ", 150),
    ],
)
def test_parse_hebrew_numeral(numeral, expected):
    assert parse_hebrew_numeral(numeral) == expected


def test_empty_is_zero():
    assert parse_hebrew_numeral("") == 0
    assert parse_hebrew_numeral("-") == 0

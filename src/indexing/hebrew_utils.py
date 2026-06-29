import re

_LETTER_VALUES: dict[str, int] = {
    'א': 1,  'ב': 2,  'ג': 3,  'ד': 4,  'ה': 5,
    'ו': 6,  'ז': 7,  'ח': 8,  'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90,
    'ק': 100,'ר': 200,'ש': 300,'ת': 400,
    'ך': 20, 'ם': 40, 'ן': 50, 'ף': 80, 'ץ': 90,
}

_INT_TO_LETTER: list[tuple[int, str]] = [
    (400, 'ת'), (300, 'ש'), (200, 'ר'), (100, 'ק'),
    (90, 'צ'),  (80, 'פ'),  (70, 'ע'),  (60, 'ס'),
    (50, 'נ'),  (40, 'מ'),  (30, 'ל'),  (20, 'כ'),
    (10, 'י'),  (9, 'ט'),   (8, 'ח'),   (7, 'ז'),
    (6, 'ו'),   (5, 'ה'),   (4, 'ד'),   (3, 'ג'),
    (2, 'ב'),   (1, 'א'),
]

_DIACRITICS = re.compile(r'[֑-ׇ]')
_MAQAF = re.compile(r'־')
_NON_HEBREW = re.compile(r'[^א-ת ]')


def int_to_hebrew(value: int) -> str:
    if value == 15:
        return 'ט"ו'
    if value == 16:
        return 'ט"ז'
    letters: list[str] = []
    for num, letter in _INT_TO_LETTER:
        while value >= num:
            letters.append(letter)
            value -= num
    if len(letters) > 1:
        return '"'.join([''.join(letters[:-1]), letters[-1]])
    return letters[0] if letters else ''


def parse_hebrew_numeral(s: str) -> int:
    letters = [c for c in s if c in _LETTER_VALUES]
    if not letters:
        return 0
    if len(letters) == 1:
        return _LETTER_VALUES[letters[0]]
    v = [_LETTER_VALUES[c] for c in letters]
    if len(v) == 2:
        return v[0] * 100 + v[1] if v[0] <= v[1] else v[0] + v[1]
    return v[0] * 100 + sum(v[1:]) if v[0] <= 9 else sum(v)


def clean_verse(raw_text: str) -> str:
    text = _MAQAF.sub(' ', raw_text)
    text = _DIACRITICS.sub('', text)
    text = _NON_HEBREW.sub('', text)
    return re.sub(r' +', ' ', text).strip()

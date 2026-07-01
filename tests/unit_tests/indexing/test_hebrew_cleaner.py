from indexing.hebrew_cleaner import clean, to_hebrew_words


def test_removes_nikud_and_teamim_but_keeps_sof_pasuk():
    pointed = "ֵראִׁ֖שית ָּבָ֣רא ֱאֹלִ֑הים ֵ֥את ַהָּׁשַ֖מִים ְוֵ֥את ָהָֽאֶרץ׃"
    result = clean(pointed)
    assert result == "ראשית ברא אלהים את השמים ואת הארץ׃"


def test_maqaf_becomes_word_boundary():
    assert clean("ַעל־ְּפֵ֣ני") == "על פני"


def test_paseq_is_removed():
    assert clean("ֱאֹלִ֖הים ׀ ְיִ֣הי") == "אלהים יהי"


def test_section_markers_do_not_leak_letters():
    assert clean("{ס ֵ֣אֶּלה ְבֵני") == "אלה בני"
    assert clean("}{פ ָלאֹו֙ר ֔יֹום") == "לאור יום"
    assert clean("ֶאָֽחד׃\n}").strip() == "אחד׃"


def test_collapses_whitespace_per_line():
    assert clean("ָׁשָ֑נה\xa0   ַוָּיֹֽמת") == "שנה וימת"


def test_to_hebrew_words_keeps_only_letters_and_spaces():
    assert to_hebrew_words("ראשית, ברא!  אלהים 123") == "ראשית ברא אלהים"

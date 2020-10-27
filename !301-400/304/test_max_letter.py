import pytest

from max_letter import max_letter_word

sample_text = '''It is a truth universally acknowledged, that a single man in
                    possession of a good fortune, must be in want of a wife.'''
with_numbers_text = '''20,000 Leagues Under the Sea is a 1954 American
                    Technicolor science fiction-adventure film...'''
emoji_text = 'emoji like 😃😃😃😃 are not letters'
accents_text = 'Société Générale est une des principales banques françaises'
mixed_case_text = 'Short Plays By Lady Gregory The Knickerbocker Press 1916'
hyphenated_word_text = 'six-feet-two in height'
compound_character_text = 'der Schloß is riesig'
no_repeat_characters_text = 'the quick brown fox jumped over the lazy dog'
non_ascii_symbols_text = '«¿Tiene sentido la TV pública?»'
apostrophe_in_word_text = "but we've been there already!!!"
underscore_torture_text = '"____".isalpha() is True, thus this test text'
digit_text = '99abc99 __abc__ --abc-- digits _ and - are not letters'
repeat_words_text = 'test test test test test correct-answer.'
no_words_in_text = '1, 2, 3'
empty_text = ''


@pytest.mark.parametrize("given, expected",
                         [(sample_text, ('possession', 's', 4)),
                          (with_numbers_text, ('Leagues', 'e', 2)),
                          (emoji_text, ('letters', 'e', 2)),
                          (accents_text, ('Société', 'é', 2)),
                          (mixed_case_text, ('Knickerbocker', 'k', 3)),
                          (hyphenated_word_text, ('six-feet-two', 'e', 2)),
                          (compound_character_text, ('Schloß', 's', 3)),
                          (no_repeat_characters_text, ('the', 't', 1)),
                          (non_ascii_symbols_text, ('Tiene', 'e', 2)),
                          (apostrophe_in_word_text, ("we've", 'e', 2)),
                          (underscore_torture_text, ('isalpha', 'a', 2)),
                          (digit_text, ('digits', 'i', 2)),
                          (repeat_words_text, ('correct-answer', 'r', 3)),
                          (no_words_in_text, ('', '', 0)),
                          (empty_text, ('', '', 0)),
                          ])
def test_max_letter_word(given, expected):
    result = max_letter_word(given)
    assert result == expected


@pytest.mark.parametrize("bad_input", [None, True, 1, 1.0, [], {}])
def test_max_letter_word_exceptions(bad_input):
    with pytest.raises(ValueError):
        max_letter_word(bad_input)

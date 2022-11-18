import os
import unicodedata
from pathlib import Path
from urllib.request import urlretrieve


def _remove_accents(accented: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', accented) if unicodedata.category(c) != 'Mn')


def _get_spanish_dictionary_words() -> dict:
    filename = "spanish.txt"
    # source of file
    # https://raw.githubusercontent.com/bitcoin/bips
    # /master/bip-0039/spanish.txt
    url = f"https://bites-data.s3.us-east-2.amazonaws.com/{filename}"
    tmp_folder = os.getenv("TMP", "/tmp")
    local_filepath = Path(tmp_folder) / filename
    if not Path(local_filepath).exists():
        urlretrieve(url, local_filepath)
    # return a dictionary of unaccented words to accented words
    return {_remove_accents(v): v for v in local_filepath.read_text(encoding='utf8').splitlines()}


SPANISH_WORDS = _get_spanish_dictionary_words()


def get_accentuated_sentence(
        text: str, words=None
) -> str:
    # Prevent accidental mutation of SPANISH_WORDS
    if words is None:
        words = SPANISH_WORDS
    new_words = []
    for word in text.split():
        if word in words:
            new_words.append(words[word])
        else:
            new_words.append(word)
    return ' '.join(new_words)

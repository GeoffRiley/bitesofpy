import pytest

from wiki_lorem_ipsum import wiki_lorem_ipsum, CONTENT


@pytest.mark.parametrize("sentences, expected", [
    (1, 1),
    (5, 5),
    (12, 12)
])
def test_number_of_sentences(sentences, expected):
    assert len(wiki_lorem_ipsum(CONTENT, sentences).split('. ')) == expected


def test_default_number():
    assert len(wiki_lorem_ipsum(CONTENT).split('. ')) == 5


def test_number_of_words():
    lorem = wiki_lorem_ipsum(CONTENT, 100).split('. ')
    for line in lorem:
        assert len(line.split()) < 16
        assert len(line.split()) > 4


@pytest.mark.parametrize("sentences", [0, -1])
def test_for_ValueError(sentences):
    with pytest.raises(ValueError):
        wiki_lorem_ipsum(CONTENT, sentences)


@pytest.fixture
def valid_words():
    return ['runt', 'hunting', 'mollusks', 'habitats', 'than', 'males', 'hatching', 'broadbill', 'smaller', 'a',
            'building', 'both', 'or', 'has', 'iucn', 'they', 'feeds', 'large', 'by', 'have', 'sexes', 'inhabits',
            'on', 'trapping', 'one', 'population', 'females', 'lowland', 'maroon', 'found', 'fourth', 'season',
            'genus', 'clutches', 'sumatra', 'insects', 'red', 'bird', 'is', 'nest', 'but', 'fullarticle', 'black',
            'breeds', 'cymbirhynchus', 'species', 'only', 'threatened', 'disturbed', 'and', 'to', 'it', 'with', 'dry',
            'sometimes', 'borneo', 'days', 'beak', 'in', 'that', 'will', 'the', 'underparts', 'its', 'yellow', 'two',
            'incubated', 'conspicuous', 'as', 'family', 'are', 'band', 'near', 'water', 'extensive', 'forests', 'egg',
            'macrorhynchos', 'over', 'indochina', 'upperparts', 'slightly', 'range', 'neck', 'due', 'fish', 'least',
            'blue', 'eggs', 'songbird', 'twenty', 'three', 'along', 'crustaceans', 'usually', 'for', 'deforestation',
            'concern', 'distinctive', 'asian', 'evaluated', 'secondary', 'trade', 'snails', 'full', 'article']


def test_all_words_are_correct(valid_words):
    lorem = wiki_lorem_ipsum(CONTENT, 100)
    for word in lorem.split():
        if word[-1] == '.':
            word = word[:-1]
        assert word.lower() in valid_words


def test_sentence_structure():
    lorem = wiki_lorem_ipsum(CONTENT, 15)
    assert all(sentence[0].isupper() for sentence in lorem.split('. '))

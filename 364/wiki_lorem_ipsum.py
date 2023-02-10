from random import choice, randint
from string import punctuation

import requests
from bs4 import BeautifulSoup

# FEATURED_ARTICLE = ('https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article/January_1,_2022')
FEATURED_ARTICLE = ('https://bites-data.s3.us-east-2.amazonaws.com/wiki_features_article_2022-01-01.html')
CONTENT = requests.get(FEATURED_ARTICLE).text


def wiki_lorem_ipsum(article: str = CONTENT, number_of_sentences: int = 5):
    """Create a lorem ipsum block of sentences from the words scraped from today's Wikipedia featured article

    :param article:
    :type article: str
    :param number_of_sentences:
    :type number_of_sentences: int
    :return: lorem ipsum text (Lorem ipsum is nonsense text used to test layouts for documents or websites)
    :rtype: str
    """
    if number_of_sentences < 1:
        raise ValueError('Requested number of sentences must be one or greater.')

    trx = str.maketrans(punctuation, ' ' * len(punctuation))
    soup = BeautifulSoup(article, 'html.parser')
    article_words = soup.select_one('div[class=mw-parser-output] > p').text.lower().replace('-', ' ').translate(
        trx).split()
    word_list = list(set(article_words))

    sentences = []
    for i in range(number_of_sentences):
        sentence = ' '.join([choice(word_list) for _ in range(randint(5, 15))])
        sentences.append(sentence[0].upper() + sentence[1:] + '.')

    return ' '.join(sentences)

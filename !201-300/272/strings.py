from typing import List


def common_words(sentence1: List[str], sentence2: List[str]) -> List[str]:
    """
    Input:  Two sentences - each is a  list of words in case insensitive ways.
    Output: those common words appearing in both sentences. Capital and lowercase 
            words are treated as the same word. 

            If there are duplicate words in the results, just choose one word. 
            Returned words should be sorted by word's length.
    """
    result = []
    for w1 in sentence1:
        word1 = w1.lower()
        if word1 not in result:
            for word2 in sentence2:
                if word1 == word2.lower():
                    result.append(word1)
                    break

    return sorted(result, key=lambda x: len(x))

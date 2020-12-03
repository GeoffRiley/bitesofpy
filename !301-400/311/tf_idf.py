import math
from collections import Counter

import pandas as pd


class TFIDF:
    """Calculate the term frequency  - inverse data frequency (TF-IDF) for a given corpus."""

    def __init__(self, corpus: pd.DataFrame):
        # The original Data Frame
        self.corpus = corpus

        # A dataframe to hold the tf-idf values
        self.df_tfidf = pd.DataFrame()

        # A set of all the words in the corpus
        self.words = set()

    def __call__(self) -> pd.DataFrame:
        # create initial word list
        self.generate_wordlist()

        # calculate tf for all documents
        self.calculate_tf()

        # calculate tf_idf
        self.calculate_tfidf()

        return self.df_tfidf

    def generate_wordlist(self):
        # Assume data is in column 1
        # Assumes each cell in column 1 is a string

        # Loop through rows of dataframe
        # df.values returns the columns as 2D array
        # because we have only one column, squeeze flattens the matrix
        # so we can loop through the column
        # and document becomes the actual string
        for document in self._docs_from_corpus():
            # Split string and add to words set
            self.words.update(document.split())

    def calculate_tf(self):
        # Create a Dataframe containing the Term Frequency values
        # tf for word i and document j is equal to the number of occurences n of this word in the document
        # divided by the total number of words for this document
        for document in self._docs_from_corpus():
            words = document.split()

            # The count of each word
            word_frequency = Counter(words)

            # calculate tf for each word by dividing the count by the total number of words
            tf_dict = {
                word: word_count / len(words)
                for word, word_count in word_frequency.items()
            }

            # Add the word dictionary as new row to the df_tfidf Dataframe
            # because there might be words that are new to other documents we get NaNs
            # so we replace them with a reasonable default which is 0
            self.df_tfidf = self.df_tfidf.append(tf_dict, ignore_index=True).fillna(0)

    def calculate_tfidf(self):
        # IDF = Log[ (Number of documents) /
        #            (Number of documents containing the word) ]
        number_documents = len(self.df_tfidf)

        # Iterate over all the words
        for word in self.df_tfidf:
            # How many rows (=documents) contain the word?
            # that is equal to a value greater zero because the value is the tf
            document_frequency = len(self.df_tfidf[self.df_tfidf[word] > 0])

            # if a word occurs in all documents, N = df and log(1) equals zero
            # so the word is not helpful in classifying a document
            # if a word occurs only in one document, the ratio is identical to number_documents
            # and the log10 is max -> idf score is max for this word so the word is highly distinctive
            word_idf = math.log10(number_documents / document_frequency)

            # Update df_tfidf Dataframe with idf calculation
            self.df_tfidf[word] *= word_idf

    def _docs_from_corpus(self):
        return self.corpus.values.squeeze()

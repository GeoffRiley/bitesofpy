from __future__ import annotations

import string
from typing import List

EOL_PUNCTUATION = ".!?"


class Document:
    def __init__(self) -> None:
        # it is up to you how to implement this method
        # feel free to alter this method and its parameters to your liking
        self._lines: List[str] = []

    def add_line(self, line: str, index: int = None) -> Document:
        """Add a new line to the document.

        Args:
            line (str): The line,
                expected to end with some kind of punctuation.
            index (int, optional): The place where to add the line into the document.
                If None, the line is added at the end. Defaults to None.

        Returns:
            Document: The changed document with the new line.
        """
        if index is None:
            index = len(self._lines)
        self._lines.insert(index, line)
        return self

    def swap_lines(self, index_one: int, index_two: int) -> Document:
        """Swap two lines.

        Args:
            index_one (int): The first line.
            index_two (int): The second line.

        Returns:
            Document: The changed document with the swapped lines.
        """
        self._lines[index_one], self._lines[index_two] = self._lines[index_two], self._lines[index_one]
        return self

    def merge_lines(self, indices: list) -> Document:
        """Merge several lines into a single line.

        If indices are not in a row, the merged line is added at the first index.

        Args:
            indices (list): The lines to be merged.

        Returns:
            Document: The changed document with the merged lines.
        """
        merged = []
        for i in indices:
            merged.append(self._lines[i])
        for i in sorted(indices, reverse=True):
            self._lines.pop(i)
        self.add_line(' '.join(merged), indices[0])
        return self

    def add_punctuation(self, punctuation: str, index: int) -> Document:
        """Add punctuation to the end of a sentence.

        Overwrites existing punctuation.

        Args:
            punctuation (str): The punctuation. One of EOL_PUNCTUATION.
            index (int): The line to change.

        Returns:
            Document: The document with the changed line.
        """
        self._lines[index] = Document._remove_punctuation(self._lines[index]) + punctuation
        return self

    def word_count(self) -> int:
        """Return the total number of words in the document."""
        return len(Document._remove_punctuation(self.__str__()).split())

    @property
    def words(self) -> list:
        """Return a list of unique words, sorted and case insensitive."""
        return list(sorted(set(Document._remove_punctuation(self.__str__()).lower().split())))

    @staticmethod
    def _remove_punctuation(line: str) -> str:
        """Remove punctuation from a line."""
        # you can use this function as helper method for
        # Document.word_count() and Document.words
        # or you can totally ignore it
        return ''.join(c for c in line if c not in string.punctuation)

    def __len__(self):
        """Return the length of the document (i.e. line count)."""
        return len(self._lines)

    def __str__(self):
        """Return the content of the document as string."""
        return '\n'.join(self._lines)


if __name__ == "__main__":
    # this part is only execute when you run the file and is ignored by the tests
    # you can use this section for debugging and testing
    d = (
        Document()
            .add_line("My first sentence.")
            .add_line("My second sentence.")
            .add_line("Introduction", 0)
            .merge_lines([1, 2])
    )

    print(d)
    print(len(d))
    print(d.word_count())
    print(d.words)

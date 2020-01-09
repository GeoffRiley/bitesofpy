PYBITES = "pybites"


def convert_pybites_chars(text):
    """Swap case all characters in the word pybites for the given text.
       Return the resulting string."""
    trx = str.maketrans('pybitesPYBITES', 'PYBITESpybites')
    return text.translate(trx)

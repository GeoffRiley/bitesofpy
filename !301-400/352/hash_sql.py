from hashlib import shake_128


def hash_query(query: str, length: int = 32) -> str:
    """Return a hash value for a given query.

    Args:
        query (str): An SQL query.
        length (int, optional): Length of the hash value. Defaults to 32.

    Raises:
        ValueError: Parameter length has to be greater equal 1.
        TypeError: Parameter length has to be of type integer.

    Returns:
        str: String representation of the hashed value.
    """
    if not isinstance(length, int):
        raise TypeError('Parameter length has to be of type integer')
    if length < 1:
        raise ValueError(f'Parameter length has to be greater equal 1. Invalid: ${length}')

    # we're ignoring the fact that fields and tables could be case-sensitive, so make everything lowercase
    working_query = query.lower()
    # ignore semicolons and backticks? Or Quotes
    translate_table = working_query.maketrans(working_query, working_query, ';"')
    working_query = working_query.translate(translate_table)
    # split up all terms on spaces
    terms = working_query.split()
    # make them predictable… sort them
    s_terms = sorted(terms)
    # Join them all together as one long uninterrupted string
    mangled_query = ''.join(s_terms)
    # We want a digest with a length, so that's a case for shake_128
    the_hash = shake_128()
    the_hash.update(mangled_query.encode())
    # return the requested length
    return the_hash.digest(length)

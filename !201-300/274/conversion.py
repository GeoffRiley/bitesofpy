def dec_to_base(number, base):
    """
    Input: number is the number to be converted
           base is the new base  (eg. 2, 6, or 8)
    Output: the converted number in the new base without the prefix (eg. '0b')
    """
    n = ''

    if base > 10:
        raise ValueError('Bases about 10 not catered')

    while number > 0:
        number, remainder = divmod(number, base)
        n += str(remainder)

    return int(n[::-1])

from string import ascii_uppercase


def convert(number: int, base: int = 2) -> str:
    """Converts an integer into any base between 2 and 36 inclusive

    Args:
        number (int): Integer to convert
        base (int, optional): The base to convert the integer to. Defaults to 2.

    Raises:
        Exception (ValueError): If base is less than 2 or greater than 36

    Returns:
        str: The returned value as a string
    """
    if not (2 <= base <= 36):
        raise ValueError(f'Bad base requested ({base})')
    return base_conv(number, base, '')


NUMBERS = [str(n) for n in range(10)] + list(ascii_uppercase)


def base_conv(number: int, base: int, so_far: str) -> str:
    so_far = NUMBERS[number % base] + so_far
    return so_far if number < base else base_conv(number // base, base, so_far)

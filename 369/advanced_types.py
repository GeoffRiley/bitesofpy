from typing import Iterable, List, Optional, Union, Iterator


def stars(*args: int, **kwargs: float) -> None:
    """Accepts arbitrary integer and a dictionary with float values"""
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, value)


def fib(n: int) -> Iterator[int]:
    """Accepts an integer"""
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b


def greet_all(names: Iterable[str]) -> None:
    """Accepts an iterable"""
    for name in names:
        print("Hello " + name)


def greeting(name: Optional[str] = None) -> str:
    """Accepts an optional string"""
    # Optional[str] means the same thing as Union[str, None]
    if name is None:
        name = "stranger"
    return "Hello, " + name


def normalize_id(user_id: Union[int, str]) -> str:
    """Accepts either integer or string"""
    if isinstance(user_id, int):
        return "user-{}".format(100000 + user_id)
    else:
        return user_id


def nums_below(numbers: Iterable[float], limit: float) -> List[float]:
    """Accepts an iterable of floats and a single float"""
    output = []
    for num in numbers:
        if num < limit:
            output.append(num)
    return output

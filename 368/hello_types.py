def greeting(name: str) -> str:
    """Return a greeting for given name."""
    return "Hello " + name


def headline(text: str, centered: bool = False, symbol: str = "o") -> str:
    """Return the text in title case and with additional markup.

    If centered is True, use symbol to fill spaces.
    If centered is False, title will have a line of "-" under it.
    """
    if not centered:
        return f"{text.title()}\n{'-' * len(text)}"
    else:
        return f" {text.title()} ".center(50, symbol)


class BankAccount:
    """Simple class to handle a bank account. Can only deal with integer amounts."""

    def __init__(self, initial_balance: int = 0) -> None:
        self.balance = initial_balance

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self.balance -= amount

    def overdrawn(self) -> bool:
        return self.balance < 0

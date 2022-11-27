import typer  # use typer.run and typer.Argument


def sum_numbers(a: int, b: int):
    """Sums two numbers"""
    return a + b


def main(
        a: str = typer.Argument(..., help="The value of the first summand"),
        b: str = typer.Argument(..., help="The value of the second summand")
):
    """
    CLI that allows you to add two numbers
    :param a: The value of the first summand
    :param b: The value of the second summand
    :return:
    """
    print(sum_numbers(int(a), int(b)))


if __name__ == "__main__":
    typer.run(main)

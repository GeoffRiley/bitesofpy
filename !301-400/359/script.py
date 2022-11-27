import typer


def subtract_numbers(a: int, b: int):
    return a - b


app = typer.Typer()


@app.command()
def subtract(
        a: int = typer.Argument(..., help="The value of the first summand"),
        b: int = typer.Argument(..., help="The value of the second summand"),
):
    """Command that allows you to add two numbers."""
    delta_ab = subtract_numbers(a, b)

    print(f"The delta is {delta_ab}")


@app.command()
def compare(
        c: int = typer.Argument(..., help="First number to compare against."),
        d: int = typer.Argument(
            ..., help="Second number that is compared against first number."
        ),
):
    """Command that checks whether a number d is greater than a number c."""

    STRING_TRUE = "greater"
    STRING_FALSE = "not greater"

    c_evaluation = STRING_TRUE if d > c else STRING_FALSE

    print(f"d={d} is {c_evaluation} than c={c}")

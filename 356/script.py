import typer


def sum_numbers(a: int, b: int):
    return a + b


app = typer.Typer()
state = {"verbose": False}


@app.command()
def sum(
        a: int = typer.Argument(..., help="The value of the first summand"),
        b: int = typer.Argument(..., help="The value of the second summand"),
):
    """Command that allows you to add two numbers."""
    sum_ab = sum_numbers(a, b)

    if state['verbose']:
        print(f"The sum is {sum_ab}")
    else:
        print(sum_ab)


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

    d_greater_c = d > c

    if state["verbose"]:
        c_evaluation = STRING_TRUE if d_greater_c else STRING_FALSE
        print(f"{d=} is {c_evaluation} than {c=}")
    else:
        print(f'd > c: {d_greater_c}')


@app.callback()
def main(
        verbose: bool = False
):
    """
    Have sum fun with numbers.
    """
    if verbose:
        print("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()

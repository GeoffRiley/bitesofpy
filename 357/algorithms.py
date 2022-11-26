import typer


def sum_numbers(a: int, b: int):
    return a + b


def subtract_numbers(a: int, b: int):
    return a - b


app = typer.Typer()

state = {"verbose": False}


@app.command()
def sum(
        a: int = typer.Argument(..., help="The value of the first summand"),
        b: int = typer.Argument(..., help="The value of the second summand"),
):
    """Command that allows you to add two numbers."""
    sum_ab = sum_numbers(a, b)

    if state["verbose"]:
        print(f"The sum is {sum_ab}")
    else:
        print(sum_ab)


@app.callback()
def main(verbose: bool = False):
    """
    Have some fun with algorithms.
    """
    if verbose:
        print("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()

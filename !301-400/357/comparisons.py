import typer

app = typer.Typer()

state = {"verbose": False}


@app.callback()
def main(verbose: bool = False):
    """
    Have sum fun with comparisons.
    """
    if verbose:
        print("Will write verbose output")
        state["verbose"] = True


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

    c_evaluation = STRING_TRUE if d_greater_c else STRING_FALSE

    if state["verbose"]:
        print(f"{d=} is {c_evaluation} than {c=}")
    else:
        print(f"d > c: {d_greater_c}")


if __name__ == "__main__":
    app()

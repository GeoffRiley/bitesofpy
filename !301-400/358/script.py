import typer

app = typer.Typer()


@app.command()
def main(
        name: str = typer.Argument(..., help="The name of the person to greet."),
):
    """CLI that allows you to greet a person."""

    print(f"Hello {name}!")

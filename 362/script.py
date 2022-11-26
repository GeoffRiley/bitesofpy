import typer

app = typer.Typer()


@app.command()
def main(
        name: str,
        password: str = typer.Option(..., prompt=True, confirmation_prompt=True, hide_input=True)
):
    print(f'Hello {name}. Doing something very secure with password.')
    print(f'...just kidding, here it is, very insecure: very_secure_password')  # Wow!


if __name__ == "__main__":
    app()

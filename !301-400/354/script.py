import typer


def sum_numbers(a: int, b: int):
    return a + b


def main(
        a: int = typer.Argument(..., help="The value of the first summand"),
        b: int = typer.Argument(..., help="The value of the second summand"),
        c: int = typer.Option(None, help="An optional third value to compare the sum against")
):
    """CLI that allows you to add two numbers"""

    """
    Okay, it's weird,
    we print 'The sum is ' followed by the summation of a and b
    but then we print ' and c is ' followed by 'None', 'smaller' or 'not smaller'!! 
    """
    the_sum = sum_numbers(a, b)
    if c is None:
        comp = 'None'
    elif the_sum <= c:
        comp = 'not smaller'
    else:
        comp = 'smaller'
    print(f'The sum is {the_sum} and c is {comp}')


if __name__ == "__main__":
    typer.run(main)

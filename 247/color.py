from random import sample


def gen_hex_color():
    while True:
        r, g, b = sample(range(0, 256), 3)
        yield '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()
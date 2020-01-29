THUMBS_UP, THUMBS_DOWN = '👍', '👎'


class Thumbs:
    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Expected int')
        if other == 0:
            raise ValueError('Specify a number')
        thumb = THUMBS_UP if other > 0 else THUMBS_DOWN
        c = abs(other)
        if c > 3:
            return f'{thumb} ({c}x)'
        else:
            return thumb * c

    def __rmul__(self, other):
        return self.__mul__(other)

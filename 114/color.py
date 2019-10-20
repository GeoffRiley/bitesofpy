"""Color class

The following sites were consulted:
    http://www.99colors.net/
    https://www.webucator.com/blog/2015/03/python-color-constants-module/
"""
import os
import re
import sys
import urllib.request

# PREWORK (don't modify): import colors, save to temp file and import
color_values_module = os.path.join('/tmp', 'color_values.py')
urllib.request.urlretrieve('https://bit.ly/2MSuu4z',
                           color_values_module)
sys.path.append('/tmp')

# should be importable now
from color_values import COLOR_NAMES  # noqa E402


class Color:
    """Color class.

    Takes the string of a color name and returns its RGB value.
    """

    def __init__(self, color: str):
        self.colorname = color
        self.rgb = COLOR_NAMES.get(color.upper(), None)

    @classmethod
    def hex2rgb(cls, hex_str: str) -> tuple:
        """Class method that converts a hex value into an rgb one"""
        if not re.match(r'#[0-9A-Fa-f]{6}', hex_str):
            raise ValueError()
        result = int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)
        return result

    @classmethod
    def rgb2hex(cls, rbg_tuple: tuple) -> str:
        """Class method that converts an rgb value into a hex one"""
        if len(rbg_tuple) != 3 or any((x < 0) or (x > 255) for x in rbg_tuple):
            raise ValueError()
        result = f'#{rbg_tuple[0]:02x}{rbg_tuple[1]:02x}{rbg_tuple[2]:02x}'
        return result

    def __repr__(self):
        """Returns the repl of the object"""
        return f"{self.__class__.__name__}('{self.colorname}')"

    def __str__(self):
        """Returns the string value of the color object"""
        return f'({", ".join(str(x) for x in self.rgb)})'

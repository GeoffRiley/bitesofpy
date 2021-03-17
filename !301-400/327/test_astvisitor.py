import pytest

from astvisitor import AstVisitor

CODE_BITE_EXAMPLE = """
import pandas as pd
import numpy as np
from argparse import ArgumentParser

print("this is a test")

parser = ArgumentParser()
len("12345")

df_tmp = pd.DataFrame(range(10), column=['x'])
df_tmp.loc[:, 'y'] = df_tmp[x] + 1

np.random.random()
"""

CODE_NO_BUILTING_NO_MODULES = """
a = 1+2
"""

CODE_NO_MODULES = """
a = 0
print(a)
a = 1+2
print(a)

b = [1,2,3,4,5]
print(len(b))
"""

CODE_NO_BUILTING = """
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--param1', dest='PARAM1', default=1, type=int)

cnt = Counter()
cnt.update([1,2,3,4,5,1,2,3,1,2,3,4,5])
"""

CODE_MIXED = """
import ast
from argparse import ArgumentParser
from collections import Counter
import argparse
import numpy as np

def get_counter():
    cnt = Counter()
    cnt.update([1,2,3,1,2,4,5,1,2,3,1])

def get_DataFrame():
    import pandas as pd
    return pd.DataFrame(get_counter())

if __name__ == '__main__':
    print("this is a test")

    parser = ArgumentParser()
    args = parser.parse_args()
    len("12345")

    df_tmp = get_DataFrame()

    v = np.random.power(10)
    print(v)
"""


@pytest.mark.parametrize(
    "input_code, expected_builtins, expected_builtins_call, expected_modules, expected_modules_call",
    [
        (
                CODE_BITE_EXAMPLE,  # input_code
                ["print", "range", "len"],  # expected_builtins
                {  # expected_builtins_call
                    "print": [6],
                    "len": [9],
                    "range": [11]
                },
                ["argparse", "numpy", "pandas"],  # expected_modules
                {  # expected_modules_call
                    "argparse.ArgumentParser": [8],
                    "pandas.DataFrame": [11],
                    "numpy.random.random": [14],
                },
        ),
        (
                CODE_NO_BUILTING_NO_MODULES,  # input_code
                [],  # expected_builtins
                {},  # expected_builtins_call
                [],  # expected_modules
                {}  # expected_modules_call
        ),
        (
                CODE_NO_MODULES,  # input_code
                ["print", "len"],  # expected_builtins
                {  # expected_builtins_call
                    "print": [3, 5, 8],
                    "len": [8]
                },
                [],  # expected_modules
                {}  # expected_modules_call
        ),
        (
                CODE_NO_BUILTING,  # input_code
                [],  # expected_builtins
                {},  # expected_builtins_call
                ["argparse", "collections"],  # expected_modules
                {  # expected_modules_call
                    "argparse.ArgumentParser": [5],
                    "collections.Counter": [8]
                },
        ),
        (
                CODE_MIXED,  # input_code
                ["print", "len"],  # expected_builtins
                {  # expected_builtins_call
                    "print": [16, 25],
                    "len": [20]
                },
                ["ast", "pandas", "argparse", "collections", "numpy"],  # expected_modules
                {  # expected_modules_call
                    "pandas.DataFrame": [13],
                    "argparse.ArgumentParser": [18],
                    "collections.Counter": [9],
                    "numpy.random.power": [24],
                },
        ),
        (
                "",  # input_code
                [],  # expected_builtins
                {},  # expected_builtins_call
                [],  # expected_modules
                {},  # expected_modules_call
        )
    ],
)
def test_astvisitor_nofilter(
        input_code,
        expected_builtins,
        expected_builtins_call,
        expected_modules,
        expected_modules_call,
):
    vis = AstVisitor(input_code)

    # Dear reader: Since no order is specified for the values returned by `.builtins()`, `.modules` etc,
    #              we sort the results and the expected values before comparing them. This allows for
    #              a stable comparison that doesn't fail when the ordering changes but the contents
    #              (results or expected) remain  the same.
    assert sorted(vis.builtins()) == sorted(expected_builtins)
    assert sorted(vis.modules()) == sorted(expected_modules)
    assert sorted(vis.builtins_lineno()) == sorted(expected_builtins_call)
    assert sorted(vis.modules_lineno()) == sorted(expected_modules_call)


@pytest.mark.parametrize(
    "input_code, valid_builtins, valid_modules, expected_builtins, expected_builtins_call, expected_modules, expected_modules_call",
    [
        (
                CODE_BITE_EXAMPLE,  # input_code
                ["iter"],  # valid_builtins
                ["np"],  # valid_modules
                [],  # expected_builtins
                {},  # expected_builtins_call
                ["numpy"],  # expected_modules
                {  # exxpected_modules_call
                    "numpy.random.random": [14],
                },
        ),
        (
                CODE_NO_BUILTING_NO_MODULES,  # input_code
                ["len"],  # valid_builtins
                ["pd", "argparse"],  # valid_modules
                [],  # expected_builtins
                {},  # expected_builtins_call
                [],  # expected_modules
                {}  # exxpected_modules_call
        ),
        (
                CODE_NO_MODULES,  # input_code
                ["len"],  # valid_builtins
                ["pd", "argparse"],  # valid_modules
                ["len"],  # expected_builtins
                {"len": [8]},  # expected_builtins_call
                [],  # expected_modules
                {}  # exxpected_modules_call
        ),
        (
                CODE_NO_BUILTING,  # input_code
                ["len"],  # valid_builtins
                ["pandas", "argparse"],  # valid_modules
                [],  # expected_builtins
                {},  # expected_builtins_call
                ["argparse"],  # expected_modules
                {"argparse.ArgumentParser": [5]},  # exxpected_modules_call
        ),
        (
                CODE_MIXED,  # input_code
                ["print"],  # valid_builtins
                ["np", "pd"],  # valid_modules
                ["print"],  # expected_builtins
                {  # expected_builtins_call
                    "print": [16, 25],
                },
                ["numpy", "pandas"],  # expected_modules
                {  # exxpected_modules_call
                    "pandas.DataFrame": [13],
                    "numpy.random.power": [24],
                },
        ),
    ],
)
def test_astvisitor_filter(
        input_code,
        valid_builtins,
        valid_modules,
        expected_builtins,
        expected_builtins_call,
        expected_modules,
        expected_modules_call,
):
    vis = AstVisitor(input_code)

    # Dear reader: Since no order is specified for the values returned by `.builtins()`, `.modules` etc,
    #              we sort the results and the expected values before comparing them. This allows for
    #              a stable comparison that doesn't fail when the ordering changes but the contents
    #              (results or expected) remain  the same.
    assert sorted(vis.builtins(valid_builtins)) == sorted(expected_builtins)
    assert sorted(vis.modules(valid_modules)) == sorted(expected_modules)
    assert sorted(vis.builtins_lineno(valid_builtins)) == sorted(expected_builtins_call)
    assert sorted(vis.modules_lineno(valid_modules)) == sorted(expected_modules_call)

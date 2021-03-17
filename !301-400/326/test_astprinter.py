import ast

import pytest

from astprinter import AstPrinter

CODE_ONE_LINE = """
one_plus_two = 1+2
"""

CODE_ONE_LINE_AST = """
Module()
   .type_ignores: []
   .body:
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'one_plus_two'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Constant()
                     .kind: None
                     .value: 1
               .op:
                  Add()
               .right:
                  Constant()
                     .kind: None
                     .value: 2
"""

CODE_ONE_LINE_AST_NO_EMPTY = """
Module()
   .body:
      Assign()
         .targets:
            Name()
               .id: 'one_plus_two'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Constant()
                     .value: 1
               .op:
                  Add()
               .right:
                  Constant()
                     .value: 2
"""

CODE_TWO_LINES = """
one_plus_two = 1+2
one_plus_two+10
"""

CODE_TWO_LINES_AST = """
Module()
   .type_ignores: []
   .body:
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'one_plus_two'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Constant()
                     .kind: None
                     .value: 1
               .op:
                  Add()
               .right:
                  Constant()
                     .kind: None
                     .value: 2
      Expr()
         .value:
            BinOp()
               .left:
                  Name()
                     .id: 'one_plus_two'
                     .ctx:
                        Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .kind: None
                     .value: 10
"""

CODE_TWO_LINES_AST_NO_EMPTY = """
Module()
   .body:
      Assign()
         .targets:
            Name()
               .id: 'one_plus_two'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Constant()
                     .value: 1
               .op:
                  Add()
               .right:
                  Constant()
                     .value: 2
      Expr()
         .value:
            BinOp()
               .left:
                  Name()
                     .id: 'one_plus_two'
                     .ctx:
                        Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .value: 10
"""

CODE_MULTI_LINE = """
a = 0
print(a)

a = a+2
print(a)

b = [1,2,3,4,5]
print(len(b))
"""

CODE_MULTI_LINE_AST = """
Module()
   .type_ignores: []
   .body:
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'a'
               .ctx:
                  Store()
         .value:
            Constant()
               .kind: None
               .value: 0
      Expr()
         .value:
            Call()
               .keywords: []
               .args:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'a'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .kind: None
                     .value: 2
      Expr()
         .value:
            Call()
               .keywords: []
               .args:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'b'
               .ctx:
                  Store()
         .value:
            List()
               .ctx:
                  Load()
               .elts:
                  Constant()
                     .kind: None
                     .value: 1
                  Constant()
                     .kind: None
                     .value: 2
                  Constant()
                     .kind: None
                     .value: 3
                  Constant()
                     .kind: None
                     .value: 4
                  Constant()
                     .kind: None
                     .value: 5
      Expr()
         .value:
            Call()
               .keywords: []
               .args:
                  Call()
                     .keywords: []
                     .args:
                        Name()
                           .id: 'b'
                           .ctx:
                              Load()
                     .func:
                        Name()
                           .id: 'len'
                           .ctx:
                              Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
"""

CODE_MULTI_LINE_AST_NO_EMPTY = """
Module()
   .body:
      Assign()
         .targets:
            Name()
               .id: 'a'
               .ctx:
                  Store()
         .value:
            Constant()
               .value: 0
      Expr()
         .value:
            Call()
               .args:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .targets:
            Name()
               .id: 'a'
               .ctx:
                  Store()
         .value:
            BinOp()
               .left:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .value: 2
      Expr()
         .value:
            Call()
               .args:
                  Name()
                     .id: 'a'
                     .ctx:
                        Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .targets:
            Name()
               .id: 'b'
               .ctx:
                  Store()
         .value:
            List()
               .ctx:
                  Load()
               .elts:
                  Constant()
                     .value: 1
                  Constant()
                     .value: 2
                  Constant()
                     .value: 3
                  Constant()
                     .value: 4
                  Constant()
                     .value: 5
      Expr()
         .value:
            Call()
               .args:
                  Call()
                     .args:
                        Name()
                           .id: 'b'
                           .ctx:
                              Load()
                     .func:
                        Name()
                           .id: 'len'
                           .ctx:
                              Load()
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
"""

CODE_COMPLEX = """
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

CODE_COMPLEX_AST = """
Module()
   .type_ignores: []
   .body:
      Import()
         .names:
            alias()
               .asname: 'pd'
               .name: 'pandas'
      Import()
         .names:
            alias()
               .asname: 'np'
               .name: 'numpy'
      ImportFrom()
         .level: 0
         .module: 'argparse'
         .names:
            alias()
               .asname: None
               .name: 'ArgumentParser'
      Expr()
         .value:
            Call()
               .keywords: []
               .args:
                  Constant()
                     .kind: None
                     .value: 'this is a test'
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'parser'
               .ctx:
                  Store()
         .value:
            Call()
               .args: []
               .keywords: []
               .func:
                  Name()
                     .id: 'ArgumentParser'
                     .ctx:
                        Load()
      Expr()
         .value:
            Call()
               .keywords: []
               .args:
                  Constant()
                     .kind: None
                     .value: '12345'
               .func:
                  Name()
                     .id: 'len'
                     .ctx:
                        Load()
      Assign()
         .type_comment: None
         .targets:
            Name()
               .id: 'df_tmp'
               .ctx:
                  Store()
         .value:
            Call()
               .args:
                  Call()
                     .keywords: []
                     .args:
                        Constant()
                           .kind: None
                           .value: 10
                     .func:
                        Name()
                           .id: 'range'
                           .ctx:
                              Load()
               .func:
                  Attribute()
                     .attr: 'DataFrame'
                     .ctx:
                        Load()
                     .value:
                        Name()
                           .id: 'pd'
                           .ctx:
                              Load()
               .keywords:
                  keyword()
                     .arg: 'column'
                     .value:
                        List()
                           .ctx:
                              Load()
                           .elts:
                              Constant()
                                 .kind: None
                                 .value: 'x'
      Assign()
         .type_comment: None
         .targets:
            Subscript()
               .ctx:
                  Store()
               .slice:
                  ExtSlice()
                     .dims:
                        Slice()
                           .lower: None
                           .step: None
                           .upper: None
                        Index()
                           .value:
                              Constant()
                                 .kind: None
                                 .value: 'y'
               .value:
                  Attribute()
                     .attr: 'loc'
                     .ctx:
                        Load()
                     .value:
                        Name()
                           .id: 'df_tmp'
                           .ctx:
                              Load()
         .value:
            BinOp()
               .left:
                  Subscript()
                     .ctx:
                        Load()
                     .slice:
                        Index()
                           .value:
                              Name()
                                 .id: 'x'
                                 .ctx:
                                    Load()
                     .value:
                        Name()
                           .id: 'df_tmp'
                           .ctx:
                              Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .kind: None
                     .value: 1
      Expr()
         .value:
            Call()
               .args: []
               .keywords: []
               .func:
                  Attribute()
                     .attr: 'random'
                     .ctx:
                        Load()
                     .value:
                        Attribute()
                           .attr: 'random'
                           .ctx:
                              Load()
                           .value:
                              Name()
                                 .id: 'np'
                                 .ctx:
                                    Load()
"""

CODE_COMPLEX_AST_NO_EMPTY = """
Module()
   .body:
      Import()
         .names:
            alias()
               .asname: 'pd'
               .name: 'pandas'
      Import()
         .names:
            alias()
               .asname: 'np'
               .name: 'numpy'
      ImportFrom()
         .level: 0
         .module: 'argparse'
         .names:
            alias()
               .name: 'ArgumentParser'
      Expr()
         .value:
            Call()
               .args:
                  Constant()
                     .value: 'this is a test'
               .func:
                  Name()
                     .id: 'print'
                     .ctx:
                        Load()
      Assign()
         .targets:
            Name()
               .id: 'parser'
               .ctx:
                  Store()
         .value:
            Call()
               .func:
                  Name()
                     .id: 'ArgumentParser'
                     .ctx:
                        Load()
      Expr()
         .value:
            Call()
               .args:
                  Constant()
                     .value: '12345'
               .func:
                  Name()
                     .id: 'len'
                     .ctx:
                        Load()
      Assign()
         .targets:
            Name()
               .id: 'df_tmp'
               .ctx:
                  Store()
         .value:
            Call()
               .args:
                  Call()
                     .args:
                        Constant()
                           .value: 10
                     .func:
                        Name()
                           .id: 'range'
                           .ctx:
                              Load()
               .func:
                  Attribute()
                     .attr: 'DataFrame'
                     .ctx:
                        Load()
                     .value:
                        Name()
                           .id: 'pd'
                           .ctx:
                              Load()
               .keywords:
                  keyword()
                     .arg: 'column'
                     .value:
                        List()
                           .ctx:
                              Load()
                           .elts:
                              Constant()
                                 .value: 'x'
      Assign()
         .targets:
            Subscript()
               .ctx:
                  Store()
               .slice:
                  ExtSlice()
                     .dims:
                        Slice()
                        Index()
                           .value:
                              Constant()
                                 .value: 'y'
               .value:
                  Attribute()
                     .attr: 'loc'
                     .ctx:
                        Load()
                     .value:
                        Name()
                           .id: 'df_tmp'
                           .ctx:
                              Load()
         .value:
            BinOp()
               .left:
                  Subscript()
                     .ctx:
                        Load()
                     .slice:
                        Index()
                           .value:
                              Name()
                                 .id: 'x'
                                 .ctx:
                                    Load()
                     .value:
                        Name()
                           .id: 'df_tmp'
                           .ctx:
                              Load()
               .op:
                  Add()
               .right:
                  Constant()
                     .value: 1
      Expr()
         .value:
            Call()
               .func:
                  Attribute()
                     .attr: 'random'
                     .ctx:
                        Load()
                     .value:
                        Attribute()
                           .attr: 'random'
                           .ctx:
                              Load()
                           .value:
                              Name()
                                 .id: 'np'
                                 .ctx:
                                    Load()
"""


@pytest.mark.parametrize(
    "input_code, expected_ast",
    [
        (CODE_ONE_LINE, CODE_ONE_LINE_AST),
        (CODE_TWO_LINES, CODE_TWO_LINES_AST),
        (CODE_MULTI_LINE, CODE_MULTI_LINE_AST),
        (CODE_COMPLEX, CODE_COMPLEX_AST),
    ],
)
def test_astprinter(capsys, input_code, expected_ast):
    tree = ast.parse(input_code)
    vst = AstPrinter(show_empty=True)
    vst.visit(tree)
    captured = capsys.readouterr()

    # applying .strip() on both captured and expected output
    # to remove empty lines at the beginning and end
    assert captured.out.strip() == expected_ast.strip()


@pytest.mark.parametrize(
    "input_code, expected_ast",
    [
        (CODE_ONE_LINE, CODE_ONE_LINE_AST_NO_EMPTY),
        (CODE_TWO_LINES, CODE_TWO_LINES_AST_NO_EMPTY),
        (CODE_MULTI_LINE, CODE_MULTI_LINE_AST_NO_EMPTY),
        (CODE_COMPLEX, CODE_COMPLEX_AST_NO_EMPTY),
    ],
)
def test_astprinter_no_empty(capsys, input_code, expected_ast):
    tree = ast.parse(input_code)
    vst = AstPrinter(show_empty=False)
    vst.visit(tree)
    captured = capsys.readouterr()

    # applying .strip() on both captured and expected output
    # to remove empty lines at the beginning and end
    assert captured.out.strip() == expected_ast.strip()

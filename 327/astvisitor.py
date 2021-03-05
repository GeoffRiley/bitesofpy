import ast
import builtins
from collections import defaultdict
from pprint import pp
from typing import List, Dict


class AstVisitor(ast.NodeVisitor):
    def __init__(self, code: str = None) -> None:
        """Initialize the object

        attrs:
        -----
        - code: source code provided as text (if not None, trigger its parsing)
        - builtins: a list of builtins we want to track (if None, track all builtins)
        - modules: a list of modules we want to track (if None, track all modules)
        """
        super().__init__()
        self.all_builtins = set(dir(builtins))

        self._builtins = defaultdict(str)
        self._modules = defaultdict(str)
        self._tree = code if code is None else self.parse(code)

    def parse(self, code: str) -> ast.Module:
        """Parse input code into an AST tree"""
        tree = ast.parse(code)
        self.visit(tree)
        return tree

    def visit_Import(self, node: ast.AST) -> None:
        """Parse an ast.Import node"""
        print(f'Import {node.names}')
        pp(node)

        ##########################################################
        # add your logic to track import statements
        # note1: watch out for aliasing ;)
        ##########################################################

        # do not remove this
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.AST) -> None:
        """Parse an ast.ImportFrom node"""
        print(f'Import from {node.module}')
        pp(node)

        ##########################################################
        # add your logic to track from/import statements
        # note: watch out for aliasing ;)
        ##########################################################

        # do not remove this
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST) -> None:
        """Parse an ast.Call node"""
        fn = node.func
        if isinstance(fn, ast.Name):
            print(f'Call: {fn.id}')
        else:
            print(f'Call: {fn.attr}')
        pp(node)
        ##########################################################
        # add your logic to track call statements
        # note1: watch out for aliasing ;)
        # note2: watch out for submodule naming such as module.submodule.submodule.func() ;)
        ##########################################################

        # do not remove this
        self.generic_visit(node)

    def builtins(self, valid: List[str] = None) -> List[str]:
        """Return the list of tracked builtins functions

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        pass

    def builtins_lineno(self, valid: List[str] = None) -> Dict[str, List[int]]:
        """Return a dictionary mapping builtins to line numbers

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        pass

    def modules(self, valid: List[str] = None) -> List[str]:
        """Return a dictionary mapping module calls to line numbers, with:
        - name aliases resolves
        - names in full dotted notation

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        pass

    def modules_lineno(self, valid: List[str] = None) -> List[str]:
        """Return a dictionary mapping modules calls to line numbers (with aliasing resolved, and names in full dotted notation)

        attrs:
        ------
        - valid: optional list of builtins to search for
        """
        pass

    def report(self, valid_builtins: List[str] = None, valid_modules: List[str] = None):
        """Print on stdout builtins and modules tracking info"""
        print(f"builtins: {self.builtins(valid_builtins)}")
        print(f"modules: {self.modules(valid_modules)}")
        print(f"builtins_lineno: {self.builtins_lineno(valid_builtins)}")
        print(f"modules_lineno: {self.modules_lineno(valid_modules)}")


# a reference example
if __name__ == "__main__":
    code = """
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

    vst = AstVisitor(code)
    vst.report()

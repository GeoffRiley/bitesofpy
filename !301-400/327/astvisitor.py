import ast
import builtins
from collections import defaultdict
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

        self._modules = set()
        self._alias = defaultdict(str)
        self._functions = defaultdict(str)
        self._call_lines = defaultdict(set)
        if code is not None:
            self.parse(code)

    def parse(self, code: str) -> ast.Module:
        """Parse input code into an AST tree"""
        tree = ast.parse(code)
        self.visit(tree)
        return tree

    def visit_Import(self, node: ast.AST) -> None:
        """Parse an ast.Import node"""
        names = []
        # line = node.lineno
        for name in node.names:
            if name.asname:
                names.append(f'{name.name} as {name.asname}')
                self._alias[name.asname] = name.name
            else:
                names.append(name.name)
            self._modules.add(name.name)
        # print(f'Import {",".join(names)} @ {line}')

        # do not remove this
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.AST) -> None:
        """Parse an ast.ImportFrom node"""
        module = node.module
        # line = node.lineno
        names = []
        for name in node.names:
            if name.asname:
                names.append(f'{name.name} as {name.asname}')
                self._alias[name.asname] = name.name
            else:
                names.append(f'{module}.{name.name}')
                self._functions[name.name] = f'{module}.{name.name}'
        self._modules.add(f'{module}')
        # print(f'From {module} Import {".".join(names)} @ {line}')

        # do not remove this
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST) -> None:
        """Parse an ast.Call node"""
        fn = node.func
        line = fn.lineno
        if isinstance(fn, ast.Name):
            name = fn.id
        else:
            name = fn.attr
            inside = fn.value
            while not isinstance(inside, ast.Name):
                name = f'{inside.attr}.{name}'
                inside = inside.value
            name = f'{inside.id}.{name}'

        if name in self._functions:
            name = self._functions[name]
        parts = name.split('.', 1)
        if len(parts) > 1 and parts[0] in self._alias:
            name = f'{self._alias[parts[0]]}.{parts[1]}'
        self._call_lines[name].add(line)
        # print(f'Call: {name}() @ {line}')

        # do not remove this
        self.generic_visit(node)

    def builtins(self, valid: List[str] = None) -> List[str]:
        """Return the list of tracked builtins functions

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        result = set(self._call_lines.keys()).intersection(self.all_builtins)
        if valid:
            result = result.intersection(set(valid))
        return list(result)

    def _resolve_alias(self, name: str) -> str:
        if name in self._alias:
            return self._alias[name]
        return name

    def _resolve_alias_list(self, names: List[str]) -> List[str]:
        if names:
            return [self._resolve_alias(s) for s in names]
        return None

    def builtins_lineno(self, valid: List[str] = None) -> Dict[str, List[int]]:
        """Return a dictionary mapping builtins to line numbers

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        builtin_list = self.builtins(self._resolve_alias_list(valid))
        result = {b: list(self._call_lines[b]) for b in builtin_list}
        return result

    def modules(self, valid: List[str] = None) -> List[str]:
        """Return a dictionary mapping module calls to line numbers, with:
        - name aliases resolves
        - names in full dotted notation

        Attrs:
        ------
        - valid: optional list of builtins to search for
        """
        result = set(self._modules)
        if valid:
            result = result.intersection(set(self._resolve_alias_list(valid)))
        return list(result)

    def modules_lineno(self, valid: List[str] = None) -> Dict[str, List[int]]:
        """Return a dictionary mapping modules calls to line numbers (with aliasing resolved, and names in full dotted notation)

        attrs:
        ------
        - valid: optional list of builtins to search for
        """
        module_list = self.modules(valid)
        result = dict()
        for m, v in self._call_lines.items():
            for s in module_list:
                if m.startswith(s):
                    result[m] = v
                    break
        # result = {m: list(v) for m, v in self._call_lines.items()
        #           if any(s.startswith(m) for s in module_list)}
        return result

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
    vst.report(["print"], ["pd"])

import ast

from typing import Any, Dict


class AstPrinter(ast.NodeVisitor):
    def __init__(self, show_empty: bool = True) -> None:
        """Initialize the object

        Arguments:
        - show_empty: when is True do not show nodes that are None,
             are empty lists, are empty string
        """

        super().__init__()
        self.SHOW_EMTPY = show_empty

    def _is_node(self, obj: Any) -> bool:
        """return True if obj is an ast.AST object"""
        return isinstance(obj, ast.AST)

    def _is_list_of_nodes(self, obj: Any) -> bool:
        """return True if obj is a list ast.AST objects"""
        return isinstance(obj, list) and len(obj) > 0 and self._is_node(obj[0])

    def _get_name(self, obj: Any) -> str:
        """return obj class name"""
        return obj.__class__.__name__

    def _is_empty(self, obj: Any) -> bool:
        """return True if obj is an empty list, empty string, or None"""
        return (isinstance(obj, list) and len(obj) == 0) or obj == "" or obj is None

    def _get_attrs(self, node: ast.AST) -> Dict[str, Any]:
        """look simple attributes, and returns them as a dictionary where
        key is the attribute name, and value the attribute value
        """
        d = {}
        for attr_name, attr_value in ast.iter_fields(node):
            if (
                    not self._is_node(attr_value)
                    and not self._is_list_of_nodes(attr_value)
                    and (self.SHOW_EMTPY or not self._is_empty(attr_value))
            ):
                d[attr_name] = attr_value

        return d

    def _get_children(self, node: ast.AST) -> Dict[str, Any]:
        """look for attributes being either nodes, or list of nodes,
        and returns them as a dictionary where key is the attribute name,
        and value the attribute value
        """
        d = {}
        for attr_name, attr_value in ast.iter_fields(node):
            if self._is_node(attr_value) or self._is_list_of_nodes(attr_value):
                d[attr_name] = attr_value
        return d

    def visit(self, node, indent: int = 0):
        """trigger visit"""

        # define your logic to print the content of the tree
        #
        # you can use self._get_attrs() and self._get_children() to
        # separate the attributes in the two required types

        def con_quote(val):
            if isinstance(val, str):
                return f"'{val}'"
            return val

        print(f'{"   " * indent}{node.__class__.__name__}()')
        indent += 1
        for attr, val in sorted(self._get_attrs(node).items()):
            print(f'{"   " * indent}.{attr}: {con_quote(val)}')
        for child, val in sorted(self._get_children(node).items()):
            print(f'{"   " * indent}.{child}:')
            if type(val) != list:
                val = [val]
            for sub in val:
                self.visit(sub, indent + 1)


if __name__ == "__main__":
    code = """
one_plus_two = 1+2
one_plus_two+10
"""
    tree = ast.parse(code)
    vst = AstPrinter(show_empty=False)
    vst.visit(tree)

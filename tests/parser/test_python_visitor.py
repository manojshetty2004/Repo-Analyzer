from pathlib import Path
import ast
from code_intelligence.visitor import PythonVisitor


def test_visitor_parsing():
    code = """
import os
from pathlib import Path as PT
import sys

class MyClass:
    '''Class doc'''
    def my_method(self, x: int) -> str:
        return str(x)

def my_func(a, b=1) -> None:
    pass
"""
    visitor = PythonVisitor(Path("test_module.py"))
    tree = ast.parse(code)
    visitor.visit(tree)

    module = visitor.module
    assert module.path == Path("test_module.py")

    # Imports
    assert len(module.imports) == 3
    assert module.imports[0].module == "os"
    assert module.imports[1].module == "pathlib"
    assert module.imports[1].name == "Path"
    assert module.imports[1].alias == "PT"

    # Classes
    assert len(module.classes) == 1
    cls = module.classes[0]
    assert cls.name == "MyClass"
    assert cls.docstring == "Class doc"
    assert len(cls.methods) == 1
    assert cls.methods[0].name == "my_method"

    # Functions
    assert len(module.functions) == 1
    func = module.functions[0]
    assert func.name == "my_func"

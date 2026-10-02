from code_intelligence.analysis import knowledge_graph_builder
from code_intelligence.analysis import knowledge_graph_builder
from code_intelligence.analysis import knowledge_graph_builder
from pathlib import Path
import ast

from code_intelligence.models import (
    ModuleInfo,
    ImportInfo,
    ParameterInfo,
    FunctionInfo,
    ClassInfo,
)


class PythonVisitor(ast.NodeVisitor):
    """
    Visits Python AST nodes and builds a ModuleInfo object.
    """

    def __init__(self, file_path: Path) -> None:
        self.module = ModuleInfo(path=file_path)
        self._module_name = file_path.stem
        self._current_class: str | None = None
        self._current_function: FunctionInfo | None = None

    def visit_Import(self, node: ast.Import) -> None:
        """
        Handles:
            import os
            import numpy as np
        """

        for alias in node.names:
            self.module.imports.append(
                ImportInfo(
                    module=alias.name,
                    alias=alias.asname,
                )
            )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        Handles:
            from pathlib import Path
        """

        module_name = node.module or ""

        for alias in node.names:
            self.module.imports.append(
                ImportInfo(
                    module=module_name,
                    name=alias.name,
                    alias=alias.asname,
                )
            )

        self.generic_visit(node)

    def _is_overload(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        for decorator in node.decorator_list:
            dec_name = ast.unparse(decorator).strip().split("(")[0].strip()
            if dec_name in ("overload", "t.overload", "typing.overload"):
                return True
        return False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self._is_overload(node):
            return

        function = self._build_function(node, is_async=False)

        previous_function = self._current_function
        self._current_function = function

        if self._current_class:
            for cls in self.module.classes:
                if cls.name == self._current_class:
                    cls.methods.append(function)
                    break
        else:
            self.module.functions.append(function)

        self.generic_visit(node)

        self._current_function = previous_function

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        if self._is_overload(node):
            return

        function = self._build_function(node, is_async=True)    
        previous_function = self._current_function    
        self._current_function = function


        if self._current_class:
            for cls in self.module.classes:
                if cls.name == self._current_class:
                    cls.methods.append(function)
                    break
        else:   
            self.module.functions.append(function)

        self.generic_visit(node)

        self._current_function = previous_function

    def visit_Call(
    self,
    node: ast.Call,
) -> None:
        """
        Handles function calls inside functions.
        """
    
        if self._current_function is None:
            self.generic_visit(node)
            return
    
        function_name = ast.unparse(node.func)
    
        self._current_function.called_functions.append(
            function_name
        )
    
        self.generic_visit(node)
    
    def _build_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        is_async: bool,
    ) -> FunctionInfo:

        if self._current_function:
            qualified_name = (
                f"{self._current_function.qualified_name}.{node.name}"
            )
        elif self._current_class:
            qualified_name = (
                f"{self._module_name}."
                f"{self._current_class}."
                f"{node.name}"
            )
        else:
            qualified_name = (
                f"{self._module_name}.{node.name}"
            )

        return FunctionInfo(
            name=node.name,
            qualified_name=qualified_name,
            parameters=self._parse_parameters(node),
            return_type=self._parse_return_type(node),
            decorators=self._parse_decorators(
                node.decorator_list
            ),
            docstring=ast.get_docstring(node),
            start_line=node.lineno,
            end_line=node.end_lineno,
            is_async=is_async,
        )

    def _parse_parameters(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> list[ParameterInfo]:

        parameters = []

        defaults = list(node.args.defaults)
        default_start = len(node.args.args) - len(defaults)

        for index, argument in enumerate(node.args.args):

            annotation = (
                ast.unparse(argument.annotation)
                if argument.annotation
                else None
            )

            default = None

            if index >= default_start:
                default_node = defaults[
                    index - default_start
                ]
                default = ast.unparse(default_node)

            parameters.append(
                ParameterInfo(
                    name=argument.arg,
                    annotation=annotation,
                    default=default,
                )
            )

        return parameters

    def _parse_return_type(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> str | None:

        if node.returns:
            return ast.unparse(node.returns)

        return None

    def _parse_decorators(
        self,
        decorators: list[ast.expr],
    ) -> list[str]:

        return [
            ast.unparse(decorator)
            for decorator in decorators
        ]

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Handles:
            class MyClass(Base1, Base2):
                ...
        """
        qualified_name = f"{self._module_name}.{node.name}"

        cls = ClassInfo(
            name=node.name,
            qualified_name=qualified_name,
            base_classes=[ast.unparse(base) for base in node.bases],
            decorators=self._parse_decorators(node.decorator_list),
            docstring=ast.get_docstring(node),
            methods=[],
            start_line=node.lineno,
            end_line=node.end_lineno,
        )
        self.module.classes.append(cls)

        previous_class = self._current_class
        self._current_class = node.name

        self.generic_visit(node)

        self._current_class = previous_class
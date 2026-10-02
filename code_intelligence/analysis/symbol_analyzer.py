from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ClassInfo,
    FunctionInfo,
)

from code_intelligence.analysis.models import (
    RepositorySymbolTable,
    SymbolInfo,
    Symbolkind,
)

class RepositorySymbolAnalyzer:
    def anlyzer(self,repository:RepositoryCodeModel,)->RepositorySymbolTable:
        table=RepositorySymbolTable()
        for module in repository.modules:
            self._add_module(table,module)

        return table

    def _add_module(self,table:RepositorySymbolTable,module:ModuleInfo,)->None:
        table.symbols.append(
            SymbolInfo(
                name=module.path.stem,
                qualified_name=module.path.stem,
                kind=Symbolkind.MODULE,
                module_path=module.path,
                line=1,
            )
        )
        for cls in module.classes:
            self._add_class(table, module, cls)

        for function in module.functions:
            self._add_function(table, module, function)

    def _add_class(
        self,
        table: RepositorySymbolTable,
        module: ModuleInfo,
        cls: ClassInfo,
    ) -> None:

        table.symbols.append(
            SymbolInfo(
                name=cls.name,
                qualified_name=cls.qualified_name,
                kind=Symbolkind.CLASS,
                module_path=module.path,
                line=cls.start_line,
            )
        )

        for method in cls.methods:
            self._add_method(table, module, method)


    def _add_function(
        self,
        table: RepositorySymbolTable,
        module: ModuleInfo,
        function: FunctionInfo,
    ) -> None:

        table.symbols.append(
            SymbolInfo(
                name=function.name,
                qualified_name=function.qualified_name,
                kind=Symbolkind.FUNCTION,
                module_path=module.path,
                line=function.start_line,
            )
        )

    def _add_method(
        self,
        table: RepositorySymbolTable,
        module: ModuleInfo,
        method: FunctionInfo,
    ) -> None:

        table.symbols.append(
            SymbolInfo(
                name=method.name,
                qualified_name=method.qualified_name,
                kind=Symbolkind.METHOD,
                module_path=module.path,
                line=method.start_line,
            )
        )

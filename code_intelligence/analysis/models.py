from pydantic import StrictStr
from enum import Enum
from pathlib import Path
from pydantic import BaseModel,Field

class Symbolkind(str,Enum):

    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"

class SymbolInfo(BaseModel):
    name:str
    qualified_name:str 
    kind:Symbolkind
    module_path:Path
    line:int

class RepositorySymbolTable(BaseModel):
    symbols:list[SymbolInfo]=Field(default_factory=list)



class ModuleConnection(BaseModel):
    module: str
    connections: int


class ArchitectureReport(BaseModel):
    modules: list[str]
    dependencies: dict[str, list[str]]
    entry_points: list[str]
    leaf_modules: list[str]
    most_connected: list[ModuleConnection]

class RepositoryStatistics(BaseModel):
    """
    High-level statistics about the repository.
    """

    total_modules: int
    total_classes: int
    total_functions: int
    total_methods: int
    total_imports: int
    total_graph_nodes: int
    total_graph_edges: int

class ModuleCoupling(BaseModel):
    module: str
    incoming_dependencies: int
    outgoing_dependencies: int
    total_dependencies: int


class CouplingReport(BaseModel):
    modules: list[ModuleCoupling]



class DeadCodeReport(BaseModel):
    unused_modules: list[str]
    unused_classes: list[str]
    unused_functions: list[str]

class CircularDependencyReport(BaseModel):
    cycles: list[list[str]]

class ModuleComplexity(BaseModel):
    module: str
    classes: int
    functions: int
    methods: int
    imports: int
    outgoing_calls: int
    complexity_score: int


class ComplexityReport(BaseModel):
    modules: list[ModuleComplexity]


class DuplicateCodeGroup(BaseModel):
    hash: str
    chunks: list[str]


class DuplicateCodeReport(BaseModel):
    duplicates: list[DuplicateCodeGroup] = Field(default_factory=list)
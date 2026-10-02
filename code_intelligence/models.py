from pydantic import BaseModel,Field
from pathlib import Path


class ImportInfo(BaseModel):
    """
    Represents one import statement.
    """

    module: str

    name: str | None = None

    alias: str | None = None





class ParameterInfo(BaseModel):
    """
    Represents a function parameter.
    """

    name: str

    annotation: str | None = None

    default: str | None = None



class FunctionInfo(BaseModel):
    """
    Represents one function or method.
    """
    qualified_name: str | None = None
    name: str

    parameters: list[ParameterInfo] = Field(default_factory=list)

    return_type: str | None = None

    decorators: list[str] = Field(default_factory=list)

    docstring: str | None = None

    start_line: int

    end_line: int

    is_async: bool = False

    called_functions: list[str] = Field(default_factory=list)

    source_code: str | None = None


class ClassInfo(BaseModel):
    """
    Represents one Python class.
    """
    qualified_name: str | None = None
    name: str

    base_classes: list[str] = Field(default_factory=list)

    decorators: list[str] = Field(default_factory=list)

    docstring: str | None = None

    methods: list[FunctionInfo] = Field(default_factory=list)

    start_line: int

    end_line: int

    source_code: str | None = None


class ModuleInfo(BaseModel):
    """
    Represents one Python module.
    """

    path: Path

    imports: list[ImportInfo] = Field(default_factory=list)

    classes: list[ClassInfo] = Field(default_factory=list)

    functions: list[FunctionInfo] = Field(default_factory=list)


class RepositoryCodeModel(BaseModel):
    """
    Represents an entire repository.
    """

    modules: list[ModuleInfo] = Field(default_factory=list)
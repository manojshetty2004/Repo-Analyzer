from enum import Enum
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"


class EdgeType(str, Enum):
    OWNS = "owns"
    INHERITS = "inherits"
    IMPORTS = "imports"
    CALLS = "calls"


class GraphNode(BaseModel):
    id: str
    name: str
    qualified_name: str
    type: NodeType


class GraphEdge(BaseModel):
    source: str
    target: str
    type: EdgeType


class RepositoryKnowledgeGraph(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)

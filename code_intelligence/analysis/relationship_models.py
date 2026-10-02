from enum import Enum

from pydantic import BaseModel, Field


class RelationshipKind(str, Enum):
    """
    Represents the type of relationship between two symbols.
    """

    OWNS = "owns"
    INHERITS = "inherits"
    IMPORTS = "imports"
    CALLS = "calls"


class RelationshipInfo(BaseModel):
    """
    Represents a relationship between two symbols.
    """

    source: str
    target: str
    kind: RelationshipKind


class RepositoryRelationshipModel(BaseModel):
    """
    Stores every relationship discovered in the repository.
    """

    relationships: list[RelationshipInfo] = Field(default_factory=list)
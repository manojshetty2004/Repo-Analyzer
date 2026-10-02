# code_intelligence/vector_store/base.py

from abc import ABC, abstractmethod
from pydantic import BaseModel
from code_intelligence.embeddings.base import EmbeddedChunk


class SearchResult(BaseModel):
    """
    A single vector search hit, ranked by similarity.
    """
    chunk_id: str
    content: str
    metadata: dict
    score: float  # similarity score, higher = more relevant


class VectorStore(ABC):
    """
    Abstraction over any vector database backend.
    No caller outside this package should know which
    engine (Chroma, Qdrant, etc.) is actually in use.
    """

    @abstractmethod
    def add(self, embedded_chunks: list[EmbeddedChunk]) -> None:
        ...

    @abstractmethod
    def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        ...

    @abstractmethod
    def delete(self, chunk_ids: list[str]) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...
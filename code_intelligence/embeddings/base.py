from abc import ABC, abstractmethod
from code_intelligence.chunking.models import EmbeddedChunk



class EmbeddingProvider(ABC):
    """
    Abstract interface for embedding providers.

    Implementations are responsible for converting text into
    embedding vectors.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError
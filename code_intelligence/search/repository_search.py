from code_intelligence.embeddings.base import EmbeddingProvider
from code_intelligence.vector_store.base import VectorStore, SearchResult


class RepositorySearchService:
    """
    Service responsible for semantic search over an indexed repository.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ):
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Search the repository for code relevant to a natural language query.

        Args:
            query: User's search query.
            top_k: Number of results to return.

        Returns:
            List of SearchResult objects.
        """

        embedding = self._embedding_provider.embed(query)

        return self._vector_store.search(query_embedding=embedding, top_k=top_k)
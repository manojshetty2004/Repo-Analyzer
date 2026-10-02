from code_intelligence.chunking.chunker import CodeChunker
from code_intelligence.embeddings.base import EmbeddingProvider
from code_intelligence.repository_parser import RepositoryParser
from code_intelligence.vector_store.base import VectorStore
from code_intelligence.chunking.models import CodeChunk, EmbeddedChunk
from code_intelligence.models import RepositoryCodeModel


class RepositoryIndexer:

    def __init__(
        self,
        parser: RepositoryParser,
        chunker: CodeChunker,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ):
        self._parser = parser
        self._chunker = chunker
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index(self, repository_path: str) -> None:

        repository = self._parser.parse(repository_path)

        chunks = self._chunker.build_chunks(repository)

        self.index_model(repository, chunks)

    def index_model(self, repository: RepositoryCodeModel, chunks: list[CodeChunk]) -> None:
        # Clear vector store first to prevent cross-repository chunk pollution
        self._vector_store.clear()

        # Deduplicate chunks by ID to prevent database unique constraint errors
        unique_chunks = []
        seen_ids = set()
        for chunk in chunks:
            if chunk.id not in seen_ids:
                unique_chunks.append(chunk)
                seen_ids.add(chunk.id)

        texts = [chunk.content for chunk in unique_chunks]
        embeddings = self._embedding_provider.embed_batch(texts)
        embedded_chunks = [
            EmbeddedChunk(chunk=chunk, embedding=emb)
            for chunk, emb in zip(unique_chunks, embeddings)
        ]

        self._vector_store.add(embedded_chunks)

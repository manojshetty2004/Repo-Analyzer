# code_intelligence/vector_store/chroma_store.py

import chromadb
from chromadb.config import Settings

from code_intelligence.chunking.models import EmbeddedChunk
from code_intelligence.vector_store.base import VectorStore, SearchResult


class ChromaStore(VectorStore):
    """
    ChromaDB-backed implementation of VectorStore.
    One collection = one repository index.
    """

    def __init__(self, persist_directory: str, collection_name: str):
        self._client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name
        )

    def add(self, embedded_chunks: list[EmbeddedChunk]) -> None:
        if not embedded_chunks:
            return

        self._collection.add(
            ids=[chunk.chunk_id for chunk in embedded_chunks],
            embeddings=[chunk.embedding for chunk in embedded_chunks],
            documents=[chunk.content for chunk in embedded_chunks],
            metadatas=[chunk.metadata for chunk in embedded_chunks],
        )

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        if not results["ids"] or not results["ids"][0]:
            return []

        search_results = []
        for i in range(len(results["ids"][0])):
            distance = results["distances"][0][i]
            similarity_score = 1 - distance  # Chroma default: cosine distance

            search_results.append(
                SearchResult(
                    chunk_id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                    score=similarity_score,
                )
            )

        return search_results

    def delete(self, chunk_ids: list[str]) -> None:
        if not chunk_ids:
            return
        self._collection.delete(ids=chunk_ids)

    def clear(self) -> None:
        self._client.delete_collection(self._collection.name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection.name
        )
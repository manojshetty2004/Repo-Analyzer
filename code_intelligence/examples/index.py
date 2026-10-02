from code_intelligence.chunking.chunker import CodeChunker
from code_intelligence.embeddings.ollama import OllamaEmbeddingProvider
from code_intelligence.indexing.repository_indexer import RepositoryIndexer
from code_intelligence.repository_parser import RepositoryParser
from code_intelligence.vector_store.chroma import ChromaStore


parser = RepositoryParser()

chunker = CodeChunker(
    repository_name="AI Assistant"
)

embedding = OllamaEmbeddingProvider()

store = ChromaStore(
    persist_directory=".chromadb",
    collection_name="assistant",
)

indexer = RepositoryIndexer(
    parser=parser,
    chunker=chunker,
    embedding_provider=embedding,
    vector_store=store,
)

indexer.index("code_intelligence")
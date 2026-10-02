from unittest.mock import Mock
from code_intelligence.indexing.repository_indexer import RepositoryIndexer
from code_intelligence.models import RepositoryCodeModel
from code_intelligence.chunking.models import CodeChunk
from pathlib import Path


def test_indexer_flow():
    # Setup mocks
    parser = Mock()
    chunker = Mock()
    embedding_provider = Mock()
    vector_store = Mock()

    # Mock return values
    repo = RepositoryCodeModel(modules=[])
    parser.parse.return_value = repo

    chunk = CodeChunk(
        id="foo.py:foo",
        repository="test",
        module_path=Path("foo.py"),
        symbol_name="foo",
        symbol_type="function",
        start_line=1,
        end_line=2,
        content="def foo(): pass",
    )
    chunker.build_chunks.return_value = [chunk]
    embedding_provider.embed_batch.return_value = [[0.1, 0.2]]

    indexer = RepositoryIndexer(
        parser=parser,
        chunker=chunker,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    indexer.index("test_repo")

    # Assertions
    parser.parse.assert_called_once_with("test_repo")
    chunker.build_chunks.assert_called_once_with(repo)
    embedding_provider.embed_batch.assert_called_once_with(["def foo(): pass"])

    # Check that vector store add is called with correct embedded chunks
    vector_store.add.assert_called_once()
    args, kwargs = vector_store.add.call_args
    embedded_chunks = args[0]
    assert len(embedded_chunks) == 1
    assert embedded_chunks[0].chunk == chunk
    assert embedded_chunks[0].embedding == [0.1, 0.2]

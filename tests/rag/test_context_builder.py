from code_intelligence.context.context_builder import ContextBuilder
from code_intelligence.vector_store.base import SearchResult


def test_context_builder_formatting():
    results = [
        SearchResult(
            chunk_id="foo.py:foo",
            content="def foo(): pass",
            metadata={
                "module_path": "foo.py",
                "symbol_name": "foo",
                "symbol_type": "function",
            },
            score=0.9,
        ),
        SearchResult(
            chunk_id="bar.py:bar",
            content="def bar(): pass",
            metadata={
                "module_path": "bar.py",
                "symbol_name": "bar",
                "symbol_type": "function",
            },
            score=0.8,
        ),
    ]

    builder = ContextBuilder()
    context = builder.build(results)

    assert "File: foo.py" in context
    assert "Symbol: foo" in context
    assert "Type: function" in context
    assert "def foo(): pass" in context

    assert "File: bar.py" in context
    assert "Symbol: bar" in context
    assert "def bar(): pass" in context


def test_context_builder_empty():
    builder = ContextBuilder()
    context = builder.build([])
    assert context == "No relevant repository context found."

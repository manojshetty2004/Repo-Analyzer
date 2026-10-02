from code_intelligence.rag.graph_context_builder import GraphContextBuilder
from code_intelligence.vector_store.base import SearchResult


def test_graph_context_builder():
    results = [
        SearchResult(
            chunk_id="foo.py:MyClass",
            content="Class: MyClass\nInherits: BaseClass\nMethods: method_a, method_b",
            metadata={
                "symbol_name": "MyClass",
                "symbol_type": "class",
                "module_path": "foo.py",
            },
            score=0.9,
        ),
        SearchResult(
            chunk_id="foo.py:func_a",
            content="Function: func_a\nCalls: func_b, MyClass.method_a",
            metadata={
                "symbol_name": "func_a",
                "symbol_type": "function",
                "module_path": "foo.py",
            },
            score=0.9,
        ),
    ]

    builder = GraphContextBuilder()
    context = builder.build(results)

    assert "- Class `MyClass` inherits from `BaseClass`" in context
    assert "- Class `MyClass` contains method `method_a`" in context
    assert "- Class `MyClass` contains method `method_b`" in context
    assert "- Function/Method `func_a` calls `func_b`" in context
    assert "- Function/Method `func_a` calls `MyClass.method_a`" in context


def test_graph_context_builder_empty():
    builder = GraphContextBuilder()
    context = builder.build([])
    assert context == "No explicit symbol relationships found in the retrieved context."

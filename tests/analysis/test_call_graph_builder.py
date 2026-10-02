from pathlib import Path
from code_intelligence.analysis.call_graph_builder import CallGraphBuilder
from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    EdgeType,
)
from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    FunctionInfo,
)


def test_call_graph_builder():
    graph = RepositoryKnowledgeGraph(nodes=[], edges=[])

    # Repository model with function call statements
    repository = RepositoryCodeModel(
        modules=[
            ModuleInfo(
                path=Path("foo.py"),
                functions=[
                    FunctionInfo(
                        name="func_a",
                        qualified_name="foo.func_a",
                        called_functions=["bar.func_b"],
                        start_line=1,
                        end_line=5,
                    )
                ],
            )
        ]
    )

    builder = CallGraphBuilder()
    updated_graph = builder.build(repository, graph)

    calls_edges = [
        (e.source, e.target)
        for e in updated_graph.edges
        if e.type == EdgeType.CALLS
    ]
    assert len(calls_edges) == 1
    assert ("foo.func_a", "bar.func_b") in calls_edges

from pathlib import Path
from code_intelligence.analysis.dependency_analyzer import DependencyAnalyzer
from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    NodeType,
    EdgeType,
)
from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ImportInfo,
)


def test_dependency_analyzer():
    # Setup initial graph containing the module nodes
    graph = RepositoryKnowledgeGraph(
        nodes=[
            GraphNode(
                id="foo", name="foo", qualified_name="foo", type=NodeType.MODULE
            ),
            GraphNode(
                id="bar", name="bar", qualified_name="bar", type=NodeType.MODULE
            ),
        ],
        edges=[],
    )
    index = GraphIndex(graph)

    # Repository model with import statements
    repository = RepositoryCodeModel(
        modules=[
            ModuleInfo(path=Path("foo.py"), imports=[ImportInfo(module="bar")]),
            ModuleInfo(path=Path("bar.py"), imports=[]),
        ]
    )

    analyzer = DependencyAnalyzer(index)
    updated_graph = analyzer.analyze(repository, graph)

    imports_edges = [
        (e.source, e.target)
        for e in updated_graph.edges
        if e.type == EdgeType.IMPORTS
    ]
    assert len(imports_edges) == 1
    assert ("foo", "bar") in imports_edges

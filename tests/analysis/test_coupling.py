from code_intelligence.analysis.coupling_analyzer import CouplingAnalyzer
from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    GraphEdge,
    NodeType,
    EdgeType,
)


def test_coupling_analyzer():
    # Construct a repository graph:
    # 2 modules: "foo" and "bar"
    # - "foo" imports "bar"
    graph = RepositoryKnowledgeGraph(
        nodes=[
            GraphNode(
                id="foo", name="foo", qualified_name="foo", type=NodeType.MODULE
            ),
            GraphNode(
                id="bar", name="bar", qualified_name="bar", type=NodeType.MODULE
            ),
        ],
        edges=[GraphEdge(source="foo", target="bar", type=EdgeType.IMPORTS)],
    )
    index = GraphIndex(graph)

    analyzer = CouplingAnalyzer(index)
    report = analyzer.analyze()

    couplings = {c.module: c for c in report.modules}
    assert "foo" in couplings
    assert "bar" in couplings

    # foo outgoing = 1, incoming = 0
    assert couplings["foo"].outgoing_dependencies == 1
    assert couplings["foo"].incoming_dependencies == 0
    assert couplings["foo"].total_dependencies == 1

    # bar outgoing = 0, incoming = 1
    assert couplings["bar"].outgoing_dependencies == 0
    assert couplings["bar"].incoming_dependencies == 1
    assert couplings["bar"].total_dependencies == 1

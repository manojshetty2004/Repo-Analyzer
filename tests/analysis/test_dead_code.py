from code_intelligence.analysis.dead_code_detector import DeadCodeDetector
from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    GraphEdge,
    NodeType,
    EdgeType,
)


def test_dead_code_detector():
    # Construct a repository graph:
    # 2 modules: "main_mod", "unused_mod"
    # 2 functions: "used_func", "unused_func"
    # 2 classes: "used_class", "unused_class"
    # - "main_mod" imports nothing
    # - "main_mod" calls "used_func" and instantiates/calls "used_class"
    # - "unused_mod" is never imported
    graph = RepositoryKnowledgeGraph(
        nodes=[
            GraphNode(
                id="main_mod",
                name="main_mod",
                qualified_name="main_mod",
                type=NodeType.MODULE,
            ),
            GraphNode(
                id="unused_mod",
                name="unused_mod",
                qualified_name="unused_mod",
                type=NodeType.MODULE,
            ),
            GraphNode(
                id="used_class",
                name="used_class",
                qualified_name="main_mod.used_class",
                type=NodeType.CLASS,
            ),
            GraphNode(
                id="unused_class",
                name="unused_class",
                qualified_name="main_mod.unused_class",
                type=NodeType.CLASS,
            ),
            GraphNode(
                id="used_func",
                name="used_func",
                qualified_name="main_mod.used_func",
                type=NodeType.FUNCTION,
            ),
            GraphNode(
                id="unused_func",
                name="unused_func",
                qualified_name="main_mod.unused_func",
                type=NodeType.FUNCTION,
            ),
        ],
        edges=[
            GraphEdge(source="main_mod", target="used_class", type=EdgeType.OWNS),
            GraphEdge(source="main_mod", target="used_func", type=EdgeType.OWNS),
            GraphEdge(
                source="main_mod", target="unused_func", type=EdgeType.OWNS
            ),
            # calls/references
            GraphEdge(source="main_mod", target="used_func", type=EdgeType.CALLS),
            GraphEdge(source="main_mod", target="used_class", type=EdgeType.CALLS),
        ],
    )
    index = GraphIndex(graph)

    detector = DeadCodeDetector(index)
    report = detector.analyze()

    assert "unused_mod" in report.unused_modules
    assert "main_mod" in report.unused_modules

    assert "main_mod.unused_class" in report.unused_classes
    assert "used_class" not in report.unused_classes


    assert "main_mod.unused_func" in report.unused_functions
    assert "used_func" not in report.unused_functions


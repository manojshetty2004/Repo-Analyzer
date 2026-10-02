from code_intelligence.analysis.complexity_analyzer import ComplexityAnalyzer
from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    GraphEdge,
    NodeType,
    EdgeType,
)


def test_complexity_analyzer():
    # Construct a repository graph:
    # 1 module "my_module"
    # - owns 1 class "MyClass"
    # - owns 1 function "my_func"
    # - class owns 1 method "my_method"
    # - module imports "other_module"
    # - function calls "other_func"
    graph = RepositoryKnowledgeGraph(
        nodes=[
            GraphNode(
                id="my_module",
                name="my_module",
                qualified_name="my_module",
                type=NodeType.MODULE,
            ),
            GraphNode(
                id="MyClass",
                name="MyClass",
                qualified_name="my_module.MyClass",
                type=NodeType.CLASS,
            ),
            GraphNode(
                id="my_func",
                name="my_func",
                qualified_name="my_module.my_func",
                type=NodeType.FUNCTION,
            ),
            GraphNode(
                id="my_method",
                name="my_method",
                qualified_name="my_module.MyClass.my_method",
                type=NodeType.METHOD,
            ),
        ],
        edges=[
            GraphEdge(source="my_module", target="MyClass", type=EdgeType.OWNS),
            GraphEdge(source="my_module", target="my_func", type=EdgeType.OWNS),
            GraphEdge(source="MyClass", target="my_method", type=EdgeType.OWNS),
            GraphEdge(
                source="my_module", target="other_module", type=EdgeType.IMPORTS
            ),
            GraphEdge(source="my_func", target="other_func", type=EdgeType.CALLS),
        ],
    )
    index = GraphIndex(graph)

    analyzer = ComplexityAnalyzer(index)
    report = analyzer.analyze()

    assert len(report.modules) == 1
    mod = report.modules[0]
    assert mod.module == "my_module"
    assert mod.classes == 1
    assert mod.functions == 1
    assert mod.methods == 0  # because class owns method, not module directly
    assert mod.imports == 1
    assert mod.outgoing_calls == 1  # because owned func my_func calls other_func
    # Score = classes (1) + functions (1) + methods (0) + imports (1) + calls (1) = 4
    assert mod.complexity_score == 4

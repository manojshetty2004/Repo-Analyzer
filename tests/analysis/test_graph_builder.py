from pathlib import Path
from code_intelligence.analysis.knowledge_graph_builder import KnowledgeGraphBuilder
from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ClassInfo,
    FunctionInfo,
)


def test_knowledge_graph_builder():
    module = ModuleInfo(
        path=Path("my_module.py"),
        classes=[
            ClassInfo(
                name="MyClass",
                qualified_name="my_module.MyClass",
                base_classes=["BaseClass"],
                methods=[
                    FunctionInfo(
                        name="my_method",
                        qualified_name="my_module.MyClass.my_method",
                        start_line=5,
                        end_line=6,
                    )
                ],
                start_line=4,
                end_line=7,
            )
        ],
        functions=[
            FunctionInfo(
                name="my_func",
                qualified_name="my_module.my_func",
                start_line=9,
                end_line=10,
            )
        ],
    )
    repo = RepositoryCodeModel(modules=[module])

    builder = KnowledgeGraphBuilder()
    graph = builder.build(repo)

    # Assert nodes
    nodes = {n.id: n for n in graph.nodes}
    assert "my_module" in nodes
    assert "my_module.MyClass" in nodes
    assert "my_module.MyClass.my_method" in nodes
    assert "my_module.my_func" in nodes

    assert nodes["my_module"].type.value == "module"
    assert nodes["my_module.MyClass"].type.value == "class"
    assert nodes["my_module.MyClass.my_method"].type.value == "method"
    assert nodes["my_module.my_func"].type.value == "function"

    # Assert edges
    owns_edges = [
        (e.source, e.target) for e in graph.edges if e.type.value == "owns"
    ]
    assert ("my_module", "my_module.MyClass") in owns_edges
    assert ("my_module", "my_module.my_func") in owns_edges
    assert ("my_module.MyClass", "my_module.MyClass.my_method") in owns_edges

    inherits_edges = [
        (e.source, e.target) for e in graph.edges if e.type.value == "inherits"
    ]
    assert ("my_module.MyClass", "BaseClass") in inherits_edges

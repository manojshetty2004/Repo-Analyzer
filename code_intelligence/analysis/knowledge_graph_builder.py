from code_intelligence.models import RepositoryCodeModel

from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    GraphEdge,
    NodeType,
    EdgeType,
)


class KnowledgeGraphBuilder:
    """
    Builds a RepositoryKnowledgeGraph from the RepositoryCodeModel.
    """

    def build(
        self,
        repository: RepositoryCodeModel,
    ) -> RepositoryKnowledgeGraph:
        """
        Build the repository knowledge graph.
        """

        graph = RepositoryKnowledgeGraph()

        for module in repository.modules:
            self._add_module(graph, module)

        return graph

    def _add_module(
        self,
        graph: RepositoryKnowledgeGraph,
        module,
    ) -> None:

        module_id = module.path.stem

        graph.nodes.append(
            GraphNode(
                id=module_id,
                name=module.path.stem,
                qualified_name=module.path.stem,
                type=NodeType.MODULE,
            )
        )

        for cls in module.classes:
            self._add_class(
                graph,
                module_id,
                cls,
            )

        for function in module.functions:
            self._add_function(
                graph,
                module_id,
                function,
            )

    def _add_class(
        self,
        graph: RepositoryKnowledgeGraph,
        module_id: str,
        cls,
    ) -> None:

        graph.nodes.append(
            GraphNode(
                id=cls.qualified_name,
                name=cls.name,
                qualified_name=cls.qualified_name,
                type=NodeType.CLASS,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=module_id,
                target=cls.qualified_name,
                type=EdgeType.OWNS,
            )
        )

        for base_class in cls.base_classes:
            graph.edges.append(
                GraphEdge(
                    source=cls.qualified_name,
                    target=base_class,
                    type=EdgeType.INHERITS,
                )
            )

        for method in cls.methods:
            self._add_method(
                graph,
                cls.qualified_name,
                method,
            )

    def _add_function(
        self,
        graph: RepositoryKnowledgeGraph,
        module_id: str,
        function,
    ) -> None:

        graph.nodes.append(
            GraphNode(
                id=function.qualified_name,
                name=function.name,
                qualified_name=function.qualified_name,
                type=NodeType.FUNCTION,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=module_id,
                target=function.qualified_name,
                type=EdgeType.OWNS,
            )
        )

    def _add_method(
        self,
        graph: RepositoryKnowledgeGraph,
        class_id: str,
        method,
    ) -> None:

        graph.nodes.append(
            GraphNode(
                id=method.qualified_name,
                name=method.name,
                qualified_name=method.qualified_name,
                type=NodeType.METHOD,
            )
        )

        graph.edges.append(
            GraphEdge(
                source=class_id,
                target=method.qualified_name,
                type=EdgeType.OWNS,
            )
        )
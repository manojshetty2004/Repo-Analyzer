from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ClassInfo,
    FunctionInfo,
)

from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphEdge,
    EdgeType,
)


class CallGraphBuilder:
    """
    Adds function call relationships to the repository knowledge graph.
    """

    def build(
        self,
        repository: RepositoryCodeModel,
        graph: RepositoryKnowledgeGraph,
    ) -> RepositoryKnowledgeGraph:
        """
        Populate the knowledge graph with CALLS edges.
        """

        for module in repository.modules:
            self._process_module(
                module,
                graph,
            )

        return graph

    def _process_module(
        self,
        module: ModuleInfo,
        graph: RepositoryKnowledgeGraph,
    ) -> None:

        for function in module.functions:
            self._process_function(
                function,
                graph,
            )

        for cls in module.classes:
            self._process_class(
                cls,
                graph,
            )

    def _process_class(
        self,
        cls: ClassInfo,
        graph: RepositoryKnowledgeGraph,
    ) -> None:

        for method in cls.methods:
            self._process_function(
                method,
                graph,
            )

    def _process_function(
        self,
        function: FunctionInfo,
        graph: RepositoryKnowledgeGraph,
    ) -> None:

        for called_function in function.called_functions:
            graph.edges.append(
                GraphEdge(
                    source=function.qualified_name,
                    target=called_function,
                    type=EdgeType.CALLS,
                )
            )
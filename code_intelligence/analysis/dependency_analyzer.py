from code_intelligence.models import (
    RepositoryCodeModel,
    ModuleInfo,
    ImportInfo,
)

from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphEdge,
    EdgeType,
)

from code_intelligence.analysis.graph_index import GraphIndex


class DependencyAnalyzer:
    """
    Builds module dependency relationships.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(
        self,
        repository: RepositoryCodeModel,
        graph: RepositoryKnowledgeGraph,
    ) -> RepositoryKnowledgeGraph:
        """
        Analyze repository dependencies.
        """

        for module in repository.modules:
            self._analyze_module(
                module,
                graph,
            )

        return graph

    def _analyze_module(
        self,
        module: ModuleInfo,
        graph: RepositoryKnowledgeGraph,
    ) -> None:
        """
        Analyze one module.
        """

        source = module.path.stem

        for import_info in module.imports:
            self._add_dependency(
                source,
                import_info,
                graph,
            )

    def _add_dependency(
        self,
        source: str,
        import_info: ImportInfo,
        graph: RepositoryKnowledgeGraph,
    ) -> None:
        """
        Add one dependency edge if the imported module exists.
        """

        target = import_info.module

        if not target:
            return

        node = self.index.get_node(target)
        if node is None:
            # Fallback to the module stem (last component of dotted name)
            last_part = target.split('.')[-1]
            node = self.index.get_node(last_part)

        if node is None:
            return

        graph.edges.append(
            GraphEdge(
                source=source,
                target=node.id,
                type=EdgeType.IMPORTS,
            )
        )
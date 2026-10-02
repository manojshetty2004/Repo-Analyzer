from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    RepositoryStatistics,
)


class RepositoryStatisticsAnalyzer:
    """
    Computes high-level statistics for the repository.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(self) -> RepositoryStatistics:
        """
        Generate repository statistics.
        """

        return RepositoryStatistics(
            total_modules=self._count_modules(),
            total_classes=self._count_classes(),
            total_functions=self._count_functions(),
            total_methods=self._count_methods(),
            total_imports=self._count_imports(),
            total_graph_nodes=self._count_graph_nodes(),
            total_graph_edges=self._count_graph_edges(),
        )

    def _count_modules(self) -> int:
        return sum(
            node.type.value == "module"
            for node in self.index.node_index.values()
        )

    def _count_classes(self) -> int:
        return sum(
            node.type.value == "class"
            for node in self.index.node_index.values()
        )

    def _count_functions(self) -> int:
        return sum(
            node.type.value == "function"
            for node in self.index.node_index.values()
        )

    def _count_methods(self) -> int:
        return sum(
            node.type.value == "method"
            for node in self.index.node_index.values()
        )

    def _count_imports(self) -> int:
        return sum(
            edge.type == EdgeType.IMPORTS
            for edge in self.index.graph.edges
        )

    def _count_graph_nodes(self) -> int:
        return len(self.index.node_index)

    def _count_graph_edges(self) -> int:
        return len(self.index.graph.edges)
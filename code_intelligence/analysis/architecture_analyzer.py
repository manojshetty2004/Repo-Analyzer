from collections import defaultdict

from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    ArchitectureReport,
    ModuleConnection,
)


class ArchitectureAnalyzer:
    """
    Analyzes the repository architecture using the knowledge graph.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index




    def analyze(self) -> ArchitectureReport:
        return ArchitectureReport(
            modules=self._analyze_modules(),
            dependencies=self._analyze_dependencies(),
            entry_points=self._find_entry_points(),
            leaf_modules=self._find_leaf_modules(),
            most_connected=[
                ModuleConnection(
                    module=name,
                    connections=count,
                )
                for name, count in self._find_most_connected_modules()
            ]
        )
    

    def _analyze_modules(self) -> list[str]:
        """
        Return all repository modules.
        """
        return sorted(
            node.qualified_name
            for node in self._module_nodes()
        )
    
    def _module_nodes(self):
        """
        Return all module nodes in the graph.
        """
        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "module"
        ]

    def _analyze_dependencies(self) -> dict[str, list[str]]:
        """
        Return module dependency map.
        """

        dependency_map = defaultdict(list)

        for edge in self.index.graph.edges:

            if edge.type != EdgeType.IMPORTS:
                continue

            dependency_map[edge.source].append(edge.target)

        return dict(dependency_map)

    def _find_entry_points(self) -> list[str]:
        """
        Modules with no incoming IMPORTS edges.
        """

        entry_points = []

        for node in self._module_nodes():

            

            incoming = [
                edge
                for edge in self.index.get_incoming_edges(node.id)
                if edge.type == EdgeType.IMPORTS
            ]

            if not incoming:
                entry_points.append(node.qualified_name)

        return sorted(entry_points)

    def _find_leaf_modules(self) -> list[str]:
        """
        Modules that import nothing.
        """

        leaves = []

        for node in self._module_nodes():

           

            outgoing = [
                edge
                for edge in self.index.get_outgoing_edges(node.id)
                if edge.type == EdgeType.IMPORTS
            ]

            if not outgoing:
                leaves.append(node.qualified_name)

        return sorted(leaves)

    def _find_most_connected_modules(
        self,
    ) -> list[tuple[str, int]]:
        """
        Return modules ordered by dependency count.
        """

        scores = []

        for node in self._module_nodes():

           

            degree = (
                len(self.index.get_outgoing_edges(node.id))
                + len(self.index.get_incoming_edges(node.id))
            )

            scores.append(
                (
                    node.qualified_name,
                    degree,
                )
            )

        scores.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scores
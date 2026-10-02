from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    CircularDependencyReport,
)


class CircularDependencyDetector:
    """
    Detect circular module dependencies.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(self) -> CircularDependencyReport:
        """
        Find all circular dependencies.
        """

        visited = set()
        stack = []
        cycles = []

        for node in self._module_nodes():

            if node.id not in visited:
                self._dfs(
                    node.id,
                    visited,
                    stack,
                    cycles,
                )

        return CircularDependencyReport(
            cycles=cycles,
        )

    def _dfs(
        self,
        node_id: str,
        visited: set[str],
        stack: list[str],
        cycles: list[list[str]],
    ) -> None:

        visited.add(node_id)
        stack.append(node_id)

        for edge in self.index.get_outgoing_edges(node_id):

            if edge.type != EdgeType.IMPORTS:
                continue

            neighbour = edge.target

            if neighbour not in visited:

                self._dfs(
                    neighbour,
                    visited,
                    stack,
                    cycles,
                )

            elif neighbour in stack:

                start = stack.index(neighbour)

                cycle = stack[start:] + [neighbour]

                readable = [
                    self.index.get_node(node).qualified_name
                    for node in cycle
                ]

                if readable not in cycles:
                    cycles.append(readable)

        stack.pop()

    def _module_nodes(self):
        """
        Return all module nodes.
        """

        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "module"
        ]
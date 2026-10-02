from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    DeadCodeReport,
)


class DeadCodeDetector:
    """
    Detects potentially unused modules, classes, and functions.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(self) -> DeadCodeReport:
        return DeadCodeReport(
            unused_modules=self._unused_modules(),
            unused_classes=self._unused_classes(),
            unused_functions=self._unused_functions(),
        )

    def _unused_modules(self) -> list[str]:
        unused = []

        for node in self._module_nodes():

            imported = any(
                edge.type == EdgeType.IMPORTS
                for edge in self.index.get_incoming_edges(node.id)
            )

            if not imported:
                unused.append(node.qualified_name)

        return sorted(unused)

    def _unused_classes(self) -> list[str]:
        unused = []

        for node in self._class_nodes():

            referenced = any(
                edge.type == EdgeType.OWNS
                for edge in self.index.get_incoming_edges(node.id)
            )

            if not referenced:
                unused.append(node.qualified_name)

        return sorted(unused)

    def _unused_functions(self) -> list[str]:
        unused = []

        for node in self._function_nodes():

            called = any(
                edge.type == EdgeType.CALLS
                for edge in self.index.get_incoming_edges(node.id)
            )

            if not called:
                unused.append(node.qualified_name)

        return sorted(unused)

    def _module_nodes(self):
        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "module"
        ]

    def _class_nodes(self):
        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "class"
        ]

    def _function_nodes(self):
        return [
            node
            for node in self.index.node_index.values()
            if node.type.value in {"function", "method"}
        ]
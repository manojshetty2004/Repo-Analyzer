from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    CouplingReport,
    ModuleCoupling,
)


class CouplingAnalyzer:
    """
    Analyzes module coupling using IMPORTS relationships.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(self) -> CouplingReport:
        modules = []

        for node in self._module_nodes():

            incoming = self._incoming_dependencies(node.id)
            outgoing = self._outgoing_dependencies(node.id)

            modules.append(
                ModuleCoupling(
                    module=node.qualified_name,
                    incoming_dependencies=incoming,
                    outgoing_dependencies=outgoing,
                    total_dependencies=incoming + outgoing,
                )
            )

        modules.sort(
            key=lambda module: module.total_dependencies,
            reverse=True,
        )

        return CouplingReport(
            modules=modules,
        )

    def _module_nodes(self):
        """
        Return all module nodes.
        """

        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "module"
        ]

    def _incoming_dependencies(
        self,
        node_id: str,
    ) -> int:
        """
        Count incoming IMPORTS edges.
        """

        return sum(
            edge.type == EdgeType.IMPORTS
            for edge in self.index.get_incoming_edges(node_id)
        )

    def _outgoing_dependencies(
        self,
        node_id: str,
    ) -> int:
        """
        Count outgoing IMPORTS edges.
        """

        return sum(
            edge.type == EdgeType.IMPORTS
            for edge in self.index.get_outgoing_edges(node_id)
        )
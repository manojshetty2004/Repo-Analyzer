from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    EdgeType,
)
from code_intelligence.analysis.models import (
    ComplexityReport,
    ModuleComplexity,
)


class ComplexityAnalyzer:
    """
    Computes high-level module complexity metrics.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def analyze(self) -> ComplexityReport:

        modules = []

        for module in self._module_nodes():

            classes = self._count_owned(module.id, "class")
            functions = self._count_owned(module.id, "function")
            methods = self._count_owned(module.id, "method")
            imports = self._count_imports(module.id)
            calls = self._count_calls(module.id)

            score = (
                classes
                + functions
                + methods
                + imports
                + calls
            )

            modules.append(
                ModuleComplexity(
                    module=module.qualified_name,
                    classes=classes,
                    functions=functions,
                    methods=methods,
                    imports=imports,
                    outgoing_calls=calls,
                    complexity_score=score,
                )
            )

        modules.sort(
            key=lambda module: module.complexity_score,
            reverse=True,
        )

        return ComplexityReport(
            modules=modules,
        )

    def _module_nodes(self):
        return [
            node
            for node in self.index.node_index.values()
            if node.type.value == "module"
        ]

    def _count_owned(
        self,
        module_id: str,
        node_type: str,
    ) -> int:

        return sum(
            edge.type == EdgeType.OWNS
            and self.index.get_node(edge.target).type.value == node_type
            for edge in self.index.get_outgoing_edges(module_id)
        )

    def _count_imports(
        self,
        module_id: str,
    ) -> int:

        return sum(
            edge.type == EdgeType.IMPORTS
            for edge in self.index.get_outgoing_edges(module_id)
        )

    def _count_calls(
        self,
        module_id: str,
    ) -> int:

        total = 0

        for edge in self.index.get_outgoing_edges(module_id):

            if edge.type != EdgeType.OWNS:
                continue

            symbol = edge.target

            total += sum(
                call.type == EdgeType.CALLS
                for call in self.index.get_outgoing_edges(symbol)
            )

        return total
from code_intelligence.analysis.graph_index import GraphIndex
from code_intelligence.analysis.knowledge_graph_models import (
    GraphNode,
    NodeType,
)


class SymbolResolver:
    """
    Resolves symbols from the knowledge graph.
    """

    def __init__(
        self,
        index: GraphIndex,
    ) -> None:
        self.index = index

    def resolve(
        self,
        symbol_name: str,
    ) -> GraphNode | None:
        """
        Resolve a symbol by its name.
        """

        for node in self.index.node_index.values():

            if node.name == symbol_name:
                return node

        return None

    def resolve_qualified_name(
        self,
        qualified_name: str,
    ) -> GraphNode | None:
        """
        Resolve a symbol by its qualified name.
        """

        return self.index.get_node(
            qualified_name
        )

    def resolve_by_type(
        self,
        symbol_name: str,
        node_type: NodeType,
    ) -> GraphNode | None:
        """
        Resolve a symbol by name and node type.
        """

        for node in self.index.node_index.values():

            if (
                node.name == symbol_name
                and node.type == node_type
            ):
                return node

        return None
from collections import defaultdict

from code_intelligence.analysis.knowledge_graph_models import (
    RepositoryKnowledgeGraph,
    GraphNode,
    GraphEdge,
)


class GraphIndex:
    """
    Builds indexes for fast graph traversal and lookup.
    """

    def __init__(
        self,
        graph: RepositoryKnowledgeGraph,
    ) -> None:

        self.graph = graph

        self.node_index: dict[str, GraphNode] = {}

        self.outgoing_edges: dict[
            str,
            list[GraphEdge]
        ] = defaultdict(list)

        self.incoming_edges: dict[
            str,
            list[GraphEdge]
        ] = defaultdict(list)

        self._build_indexes()

    def _build_indexes(self) -> None:
        """
        Build all graph indexes.
        """

        self._build_node_index()

        self._build_edge_indexes()

    def _build_node_index(self) -> None:
        """
        Index every node by its id.
        """

        for node in self.graph.nodes:
            self.node_index[node.id] = node

    def _build_edge_indexes(self) -> None:
        """
        Build incoming and outgoing edge indexes.
        """

        for edge in self.graph.edges:

            self.outgoing_edges[
                edge.source
            ].append(edge)

            self.incoming_edges[
                edge.target
            ].append(edge)

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:
        """
        Return a node by id.
        """

        return self.node_index.get(node_id)

    def get_outgoing_edges(
        self,
        node_id: str,
    ) -> list[GraphEdge]:
        """
        Return every outgoing edge.
        """

        return self.outgoing_edges.get(
            node_id,
            [],
        )

    def get_incoming_edges(
        self,
        node_id: str,
    ) -> list[GraphEdge]:
        """
        Return every incoming edge.
        """

        return self.incoming_edges.get(
            node_id,
            [],
        )
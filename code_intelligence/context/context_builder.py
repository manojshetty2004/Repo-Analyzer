from code_intelligence.vector_store.base import SearchResult


class ContextBuilder:
    """
    Builds an LLM-ready context from search results.
    """

    def build(
        self,
        results: list[SearchResult],
    ) -> str:
        """
        Convert search results into a formatted context string.
        """

        if not results:
            return "No relevant repository context found."

        sections = []

        for result in results:
            metadata = result.metadata

            section = (
                f"File: {metadata.get('module_path', 'Unknown')}\n"
                f"Symbol: {metadata.get('symbol_name', 'Unknown')}\n"
                f"Type: {metadata.get('symbol_type', 'Unknown')}\n\n"
                f"{result.content}"
            )

            sections.append(section)

        return "\n\n" + ("\n" + "-" * 80 + "\n\n").join(sections)
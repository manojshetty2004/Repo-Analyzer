class GraphContextBuilder:
    """
    Builds context about symbol relationships from search results.
    """

    def build(self, search_results: list) -> str:
        """
        Analyze search result contents to extract explicit calls, inheritance,
        and method definitions, format them, and return a relationships block.
        """
        relationships = []

        for result in search_results:
            content = getattr(result, "content", "")
            meta = getattr(result, "metadata", {})
            name = meta.get("symbol_name")

            if not name or not content:
                continue

            lines = content.split("\n")
            for line in lines:
                if line.startswith("Inherits: "):
                    bases = [b.strip() for b in line[len("Inherits: "):].split(",")]
                    for base in bases:
                        relationships.append(
                            f"- Class `{name}` inherits from `{base}`"
                        )
                elif line.startswith("Calls: "):
                    calls = [c.strip() for c in line[len("Calls: "):].split(",")]
                    for call in calls:
                        relationships.append(
                            f"- Function/Method `{name}` calls `{call}`"
                        )
                elif line.startswith("Methods: "):
                    methods = [m.strip() for m in line[len("Methods: "):].split(",")]
                    for method in methods:
                        relationships.append(
                            f"- Class `{name}` contains method `{method}`"
                        )

        if not relationships:
            return "No explicit symbol relationships found in the retrieved context."

        return "\n".join(sorted(list(set(relationships))))
from code_intelligence.routing.intent import Intent


class IntentRouter:
    """
    Determines which subsystem should answer the question.
    """

    def route(
        self,
        question: str,
    ) -> Intent:

        question = question.lower()

        #
        # Statistics
        #

        if any(
            word in question
            for word in (
                "statistics",
                "stats",
                "number of modules",
                "number of classes",
                "repository statistics",
            )
        ):
            return Intent.STATISTICS

        #
        # Architecture
        #

        if any(
            word in question
            for word in (
                "architecture",
                "entry point",
                "leaf module",
                "most connected",
            )
        ):
            return Intent.ARCHITECTURE

        #
        # Complexity
        #

        if any(
            word in question
            for word in (
                "complexity",
                "complex",
                "score",
            )
        ):
            return Intent.COMPLEXITY

        #
        # Coupling
        #

        if any(
            word in question
            for word in (
                "coupling",
                "dependencies",
                "dependency count",
            )
        ):
            return Intent.COUPLING

        #
        # Dead Code
        #

        if any(
            word in question
            for word in (
                "dead code",
                "unused",
                "unused function",
                "unused class",
            )
        ):
            return Intent.DEAD_CODE

        #
        # Duplicate Code
        #

        if any(
            word in question
            for word in (
                "duplicate",
                "duplicates",
                "copy paste",
            )
        ):
            return Intent.DUPLICATES

        #
        # Circular
        #

        if any(
            word in question
            for word in (
                "circular",
                "cycle",
                "cyclic",
            )
        ):
            return Intent.CIRCULAR

        #
        # Everything else
        #

        return Intent.RAG
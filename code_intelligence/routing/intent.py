from enum import Enum


class Intent(str, Enum):
    """
    Intents determining which analyzer or subsystem should handle the request.
    """

    STATISTICS = "statistics"
    ARCHITECTURE = "architecture"
    COMPLEXITY = "complexity"
    COUPLING = "coupling"
    DEAD_CODE = "dead_code"
    DUPLICATES = "duplicates"
    CIRCULAR = "circular"
    RAG = "rag"

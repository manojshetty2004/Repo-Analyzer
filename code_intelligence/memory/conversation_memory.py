from collections import deque

from code_intelligence.memory.models import (
    ConversationTurn,
)


class ConversationMemory:
    """
    Stores recent conversation history.

    The memory is intentionally simple.
    Later it can be replaced with a vector store
    or database without changing the RAG engine.
    """

    def __init__(
        self,
        max_history: int = 10,
    ) -> None:

        self._history = deque(
            maxlen=max_history,
        )

    def add(
        self,
        question: str,
        answer: str,
    ) -> None:

        self._history.append(
            ConversationTurn(
                question=question,
                answer=answer,
            )
        )

    def clear(self) -> None:

        self._history.clear()

    def history(self) -> list[ConversationTurn]:

        return list(self._history)

    def build_context(self) -> str:

        if not self._history:
            return ""

        lines = [
            "Previous Conversation",
            "=====================",
        ]

        for turn in self._history:

            lines.append(f"User: {turn.question}")
            lines.append(f"Assistant: {turn.answer}")
            lines.append("")

        return "\n".join(lines)
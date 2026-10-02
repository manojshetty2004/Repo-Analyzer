class PromptBuilder:

    SYSTEM_PROMPT = """
You are an expert AI Software Engineering Assistant.

Answer ONLY using:

1. Repository Context
2. Repository Relationships
3. Previous Conversation

If the answer cannot be determined,
say so.

Use previous conversation whenever it helps answer follow-up questions.
""".strip()

    def build(
        self,
        question: str,
        repository_context: str,
        graph_context: str,
        conversation_context: str,
    ) -> str:

        return f"""
{self.SYSTEM_PROMPT}

{conversation_context}

Repository Context
==================
{repository_context}

Repository Relationships
========================
{graph_context}

User Question
=============
{question}

Answer:
""".strip()
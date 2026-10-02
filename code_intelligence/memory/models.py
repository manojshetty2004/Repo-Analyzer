from pydantic import BaseModel


class ConversationTurn(BaseModel):
    """
    Represents a single turn of user-assistant interaction.
    """

    question: str
    answer: str

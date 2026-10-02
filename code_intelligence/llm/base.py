from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract base class for language model providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a text response for the given prompt.
        """
        pass

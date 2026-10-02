from langchain_ollama import ChatOllama
from code_intelligence.llm.base import LLMProvider

class OllamaLLMProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
    ):
        self._llm = ChatOllama(
            model=model,
            temperature=temperature,
        )
    
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM.
        """
        response = self._llm.invoke(prompt)
        return response.content




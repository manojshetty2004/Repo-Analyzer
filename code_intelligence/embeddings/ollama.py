from code_intelligence.embeddings.base import EmbeddingProvider
from langchain_ollama import OllamaEmbeddings
import ollama


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self,model_name:str="nomic-embed-text-v2-moe"):
        self._embeddings=OllamaEmbeddings(
            model=model_name)

    def embed(self,text:str)->list[float]:
        return self._embeddings.embed_query(text)

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        batch_size = 16
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            results.extend(self._embeddings.embed_documents(batch))
        return results


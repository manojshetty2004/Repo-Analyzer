from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text-v2-moe"
    llm_model: str = "qwen2.5:3b"
    chroma_path: str = "./chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()
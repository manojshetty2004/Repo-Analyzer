from pydantic import BaseModel,Field
from pathlib import Path

class CodeChunk(BaseModel):
    id:str=Field(
        description="unique identifieer for each chunk"
    )
    repository:str=Field(
        description="repository name"
    )
    module_path:Path=Field(
        description="path of source module"
    )
    symbol_name: str = Field(
        description="Name of the class, function, or module."
    )

    symbol_type: str = Field(
        description="Type of symbol (module, class, function, method)."
    )

    start_line: int = Field(
        description="Starting line number."
    )

    end_line: int = Field(
        description="Ending line number."
    )

    content: str = Field(
        description="Source code contained in this chunk."
    )

class EmbeddedChunk(BaseModel):
    chunk:CodeChunk
    embedding:list[float]=Field(
        description="Embedding vector for semantic search."
    )

    @property
    def chunk_id(self) -> str:
        return self.chunk.id

    @property
    def content(self) -> str:
        return self.chunk.content

    @property
    def metadata(self) -> dict:
        return {
            "repository": self.chunk.repository,
            "module_path": str(self.chunk.module_path),
            "symbol_name": self.chunk.symbol_name,
            "symbol_type": self.chunk.symbol_type,
            "start_line": self.chunk.start_line,
            "end_line": self.chunk.end_line,
        }
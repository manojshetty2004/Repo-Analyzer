from pydantic import BaseModel


class IndexRepositoryRequest(BaseModel):
    repository_path: str | None = None
    repository_url: str | None = None


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
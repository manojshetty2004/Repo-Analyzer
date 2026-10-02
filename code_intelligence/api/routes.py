from fastapi import APIRouter, HTTPException
from code_intelligence.utils.github import GitHubRepository

from code_intelligence.api.schemas import (
    AskRequest,
    AskResponse,
    IndexRepositoryRequest,
)

router = APIRouter()


_application = None


def configure(application):
    global _application
    _application = application


@router.post("/index")
def index_repository(
    request: IndexRepositoryRequest,
):
    path = request.repository_path.strip() if request.repository_path else None
    url = request.repository_url.strip() if request.repository_url else None

    if path == "string" or not path:
        path = None
    if url == "string" or not url:
        url = None

    repository = path or url

    if repository is None:
        raise HTTPException(
            status_code=400,
            detail="repository_path or repository_url is required."
        )

    try:
        _application.index(repository)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to index repository: {str(e)}"
        )

    return {
        "message": "Repository indexed successfully."
    }
    

   


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask(request: AskRequest):

    answer = _application.ask(
        request.question,
    )

    return AskResponse(
        answer=answer,
    )


@router.post("/clear")
def clear_database():
    try:
        _application._indexer._vector_store.clear()
        # Reset analysis report too
        _application._analysis._last_report = None
        return {"message": "Database cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
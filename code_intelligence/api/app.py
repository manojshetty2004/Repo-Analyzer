from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from code_intelligence.bootstrap import (
    build_application,
)

from code_intelligence.api.routes import (
    router,
    configure,
)


application = build_application()

configure(application)

app = FastAPI(
    title="AI Software Engineering Assistant",
    version="1.0.0",
)

app.include_router(router)

static_dir = Path(__file__).resolve().parent.parent.parent / "static"
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
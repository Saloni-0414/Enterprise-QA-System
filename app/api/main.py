from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Enterprise Q&A System",
    description="Enterprise document question-answering system with citations.",
    version="1.0.0"
)

app.include_router(router)

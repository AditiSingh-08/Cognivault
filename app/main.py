from fastapi import FastAPI
from app.api.document_routes import router as document_router
from app.api.query_routes import router as query_router
app = FastAPI(
    title="Cognivault API",
    description="An intelligent document question-answering system",
    version="1.0.0"
)
app.include_router(
    query_router,
    prefix="/documents",
    tags=["Documents"]
)
app.include_router(document_router, prefix="/documents", tags=["Documents"])

@app.get("/")
def home():
    return {
        "message": "Welcome to Cognivault API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Cognivault"
    }
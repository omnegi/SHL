from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommendation API",
        "health": "/health",
        "docs": "/docs",
    }
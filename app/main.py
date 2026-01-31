from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import stocks

app = FastAPI(title=settings.APP_NAME)

app.include_router(stocks.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return{
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs"
    }

@app.get("/config")
def show_config():
    return{
        "app_name": settings.APP_NAME,
        "database_url": settings.DATABASE_URL[:20] + "..."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/")
def read_root():
    return{
        "message": "Hello World",
        "app_name": settings.APP_NAME
    }

@app.get("/config")
def show_config():
    return{
        "app_name": settings.APP_NAME,
        "database_url": settings.DATABASE_URL[:20] + "..."
    }
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    ALPHA_VANTAGE_API_KEY: str
    ALPHA_VANTAGE_RATE_LIMIT: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
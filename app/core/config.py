from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ALPHA_VANTAGE_API_KEY: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "your-secret-key-here"
    
    class Config:
        env_file = ".env"

settings = Settings()

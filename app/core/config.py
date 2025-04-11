from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ALPHA_VANTAGE_API_KEY: str
    FINNHUB_API_KEY: str
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://actinovate-frontend.vercel.app"
    ]
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        env_file = ".env"

settings = Settings()

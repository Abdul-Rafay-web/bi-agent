from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Rafay\Rafay\Languages\Agentic AI\groq_api_key.env")


class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "bi_agent")

    class Config:
        env_file = ".env"


settings = Settings()

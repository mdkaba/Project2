from typing import List
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base
    DEBUG: bool = False
    PROJECT_NAME: str = "Multi-Agent Chatbot"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # Ollama
    OLLAMA_API_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "mistral"
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./data/vector_store"
    
    # External APIs
    WIKIPEDIA_API_URL: str = "https://en.wikipedia.org/w/api.php"
    ARXIV_API_URL: str = "http://export.arxiv.org/api/query"
    CONCORDIA_API_BASE_URL: str = "https://opendata.concordia.ca/API/v1/"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings()

# Ensure required directories exist
def create_directories():
    Path(settings.VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

create_directories() 
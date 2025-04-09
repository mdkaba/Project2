# backend/app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl, FilePath, DirectoryPath, computed_field
from typing import List, Union, Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # CORS Settings
    # Accepts a string like "http://localhost:3000,http://localhost:5173"
    # and converts it into a list of strings
    CORS_ORIGINS_STR: str = Field(..., validation_alias='CORS_ORIGINS')

    # Database Configuration (SQLite)
    DATABASE_URL: str

    # Ollama Configuration
    OLLAMA_API_BASE_URL: HttpUrl
    OLLAMA_MODEL_NAME: str = "mistral"

    # Vector Store Settings
    VECTOR_STORE_PATH: str

    # Github API
    GITHUB_PAT: Optional[str] = None # Optional in case not provided or needed immediately

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None # Optional path for file logging

    # Define CORS_ORIGINS as a computed field based on CORS_ORIGINS_STR
    @computed_field 
    def CORS_ORIGINS(self) -> List[str]:
        if self.CORS_ORIGINS_STR:
            return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(',')]
        return []

    def __init__(self, **values):
        super().__init__(**values)
        # Post-process CORS_ORIGINS_STR into a list
        # self.CORS_ORIGINS: List[str] = [] # Removed
        # if self.CORS_ORIGINS_STR: # Removed
        #     self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS_STR.split(',')] # Removed
        
        # Ensure parent directory for vector store exists
        if self.VECTOR_STORE_PATH:
             # Check if path is absolute or construct absolute path if relative
             abs_vector_path = self.VECTOR_STORE_PATH
             if not os.path.isabs(abs_vector_path):
                 # Assuming config.py is in backend/app/core
                 project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
                 abs_vector_path = os.path.join(project_root, abs_vector_path)
             os.makedirs(abs_vector_path, exist_ok=True)

        # Ensure parent directory for log file exists if specified
        if self.LOG_FILE:
             abs_log_path = self.LOG_FILE
             if not os.path.isabs(abs_log_path):
                 project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
                 abs_log_path = os.path.join(project_root, abs_log_path)
             log_dir = os.path.dirname(abs_log_path)
             if log_dir:
                 os.makedirs(log_dir, exist_ok=True)
                 
        # Ensure parent directory for DB file exists if specified
        if self.DATABASE_URL and self.DATABASE_URL.startswith("sqlite"):
            db_path = self.DATABASE_URL.split("///")[-1]
            # Handle potential absolute vs relative paths for DB if needed
            if not os.path.isabs(db_path):
                 project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
                 db_path = os.path.join(project_root, db_path)
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)


    class Config:
        # Specify path relative to this config.py file
        env_file = '../../../.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True # Important for environment variable names like GITHUB_PAT


# Instantiate the settings
settings = Settings()

# Example Usage (can be imported elsewhere):
# from app.core.config import settings
# print(settings.DATABASE_URL)
# print(settings.CORS_ORIGINS) 
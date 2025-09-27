"""
Application configuration management with environment validation.
"""
from functools import lru_cache
from typing import List, Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    PROJECT_NAME: str = "Vesuvian"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Fitness App"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("ALLOWED_HOSTS", mode="before")
    def assemble_allowed_hosts(cls, v: Any) -> Any:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Pydantic v2 config using SettingsConfigDict for BaseSettings
    # (assigned after class definition to avoid mypy class-variable override checks)
    pass


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Assign model_config after class definition to avoid mypy complaining about
# class variable overrides on BaseSettings.
Settings.model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

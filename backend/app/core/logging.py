"""
Logging configuration for the application.
"""
import logging
import sys
from app.core.config import get_settings


def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class LoggerMixin:
    """Mixin to add logger to classes."""
    
    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(self.__class__.__name__)

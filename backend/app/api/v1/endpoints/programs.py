"""Program management endpoints re-exported from the program domain."""

from app.domains.program.routes.programs import router

__all__ = ["router"]
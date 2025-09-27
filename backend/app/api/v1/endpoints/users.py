"""User management endpoints re-exported from the users domain."""

from app.domains.users.routes.users import router

__all__ = ["router"]

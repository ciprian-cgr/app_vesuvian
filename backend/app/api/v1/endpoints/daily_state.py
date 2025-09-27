"""Daily state management endpoints re-exported from the daily_state domain."""

from app.domains.daily_state.routes.daily_state import router

__all__ = ["router"]
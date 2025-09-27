from datetime import date, datetime, timedelta
from typing import List, Optional

from app.core.logging import LoggerMixin
from app.domains.daily_state.models import DailyState, ContextualRecommendation
from app.domains.daily_state.repositories import (
    IDailyStateRepository,
    IContextualRecommendationRepository,
)
from app.domains.daily_state.schemas import DailyStateCreate


class DailyStateService(LoggerMixin):
    def __init__(
        self,
        daily_state_repo: IDailyStateRepository,
        recommendation_repo: IContextualRecommendationRepository,
    ):
        self.daily_state_repo = daily_state_repo
        self.recommendation_repo = recommendation_repo

    async def get_daily_state(self, user_id: str, for_date: date) -> DailyState:
        """
        Retrieves the daily state for a user and date.
        If the state is missing or expired, it generates a new one.
        """
        now = datetime.utcnow()
        state = await self.daily_state_repo.get_by_user_and_date(user_id, for_date)

        if state and state.expires_at > now:
            self.logger.info(f"Returning cached daily state for user {user_id} on {for_date}.")
            return state

        self.logger.info(f"Generating new daily state for user {user_id} on {for_date}.")
        return await self._generate_new_daily_state(user_id, for_date)

    async def _generate_new_daily_state(
        self, user_id: str, for_date: date
    ) -> DailyState:
        """
        Private method to generate a new daily state.
        This would integrate with program schedules, user context, etc.
        """
        # Placeholder logic for generation
        new_state_data = DailyStateCreate(
            user_id=user_id,
            date=for_date,
            scheduled_session={"name": "Generated Workout", "details": "..."},
            daily_priorities={"focus": "Mobility"},
            relevant_progress={"milestone": "Approaching 100kg squat"},
            available_actions={"quick_log": True},
            ai_recommendations={"suggestion": "Try a lighter warm-up today."},
            expires_at=datetime.utcnow() + timedelta(hours=1), # Cache for 1 hour
        )

        # Use existing update method or create if it doesn't exist
        existing_state = await self.daily_state_repo.get_by_user_and_date(user_id, for_date)
        if existing_state:
            return await self.daily_state_repo.update(user_id, for_date, new_state_data.model_dump())
        else:
            return await self.daily_state_repo.create(new_state_data.model_dump())


    async def get_active_recommendations(
        self, user_id: str
    ) -> List[ContextualRecommendation]:
        """
        Retrieves all active (non-expired) recommendations for a user.
        """
        return await self.recommendation_repo.get_active_by_user_id(user_id)

    async def process_daily_action(self, user_id: str, action_data: dict) -> dict:
        """
        Processes a quick action from the daily view.
        This is a placeholder for more complex logic.
        """
        self.logger.info(f"Processing action {action_data.get('type')} for user {user_id}.")
        # In a real scenario, this would update the underlying program data
        # and return a result.
        return {"status": "success", "action": action_data.get("type")}
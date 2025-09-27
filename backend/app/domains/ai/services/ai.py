from typing import Optional

from app.core.logging import LoggerMixin
from app.domains.ai.models import AIContext
from app.domains.ai.repositories import IAIContextRepository
from app.domains.ai.schemas import AIContextCreate, AIContextUpdate


class AIService(LoggerMixin):
    def __init__(self, repository: IAIContextRepository):
        self.repository = repository

    async def get_or_create_ai_context(self, user_id: str) -> AIContext:
        """
        Retrieves the AI context for a user. If it doesn't exist,
        it creates a new one with default values.
        """
        context = await self.repository.get_by_user_id(user_id)
        if not context:
            self.logger.info(f"No AI context found for user {user_id}. Creating one.")
            context_create = AIContextCreate(
                user_id=user_id,
                user_preferences={},
                patterns={},
                current_state={},
            )
            context_data = context_create.model_dump()
            context = await self.repository.create(context_data)
        return context

    async def update_ai_context(
        self, user_id: str, context_update: AIContextUpdate
    ) -> Optional[AIContext]:
        """
        Updates the AI context for a user. This is where logic for
        pattern recognition and state updates will be triggered.
        """
        self.logger.info(f"Updating AI context for user {user_id}.")
        # In a real scenario, this would involve more complex logic to merge
        # and analyze the incoming context_updates.
        update_data = context_update.model_dump(exclude_unset=True)

        # Here, you could trigger other processes, like checking for adaptation triggers
        # based on the new context.

        return await self.repository.update(user_id, update_data)
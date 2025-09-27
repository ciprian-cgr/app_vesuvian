from typing import Optional, List

from app.core.logging import LoggerMixin
from app.domains.program.models import Program, TrainingCycle, Workout
from app.domains.program.repositories import (
    IProgramRepository,
    ITrainingCycleRepository,
    IWorkoutRepository,
)
from app.domains.program.schemas import ProgramCreate, ProgramUpdate


class ProgramService(LoggerMixin):
    def __init__(
        self,
        program_repo: IProgramRepository,
        cycle_repo: ITrainingCycleRepository,
        workout_repo: IWorkoutRepository,
    ):
        self.program_repo = program_repo
        self.cycle_repo = cycle_repo
        self.workout_repo = workout_repo

    async def create_program(self, program_create: ProgramCreate) -> Program:
        """
        Creates a new program, including its cycles and workouts.
        This is where the core logic for program generation will reside.
        """
        # 1. Validate program specifications (placeholder)
        self.logger.info(f"Validating program spec for user {program_create.user_id}")

        # 2. Ensure goal compatibility (placeholder)
        self.logger.info("Ensuring goal compatibility.")

        # 3. Create the core program entry
        program_data = program_create.model_dump()
        program = await self.program_repo.create(program_data)
        self.logger.info(f"Created program {program.id} for user {program.user_id}")

        # 4. Generate initial weekly schedules (placeholder)
        self.logger.info(f"Generating initial schedule for program {program.id}")
        # In a real scenario, this would involve creating TrainingCycle and Workout objects.

        # 5. Set AI confidence score (placeholder)
        program.ai_confidence_score = 0.85  # Example score
        await self.program_repo.update(program.id, {"ai_confidence_score": 0.85})

        return program

    async def get_program_by_id(self, program_id: str) -> Optional[Program]:
        return await self.program_repo.get_by_id(program_id)

    async def get_full_program_details(self, program_id: str) -> dict:
        """
        Retrieves the full program, including its cycles and their workouts.
        """
        program = await self.program_repo.get_by_id(program_id)
        if not program:
            return None

        cycles = await self.cycle_repo.get_all_by_program_id(program.id)

        workouts_by_cycle = {}
        for cycle in cycles:
            workouts = await self.workout_repo.get_all_by_cycle_id(cycle.id)
            workouts_by_cycle[cycle.id] = workouts

        return {
            "program": program,
            "cycles": cycles,
            "workouts_by_cycle": workouts_by_cycle,
        }

    async def update_program(
        self, program_id: str, program_update: ProgramUpdate
    ) -> Optional[Program]:
        update_data = program_update.model_dump(exclude_unset=True)
        return await self.program_repo.update(program_id, update_data)
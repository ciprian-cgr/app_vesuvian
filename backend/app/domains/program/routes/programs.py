from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_program_service, get_user_service
from app.domains.program.schemas import Program, ProgramCreate, ProgramUpdate
from app.domains.program.services import ProgramService
from app.domains.users.routes.users import get_current_user
from app.domains.users.schemas import User

router = APIRouter()


@router.post("/", response_model=Program, status_code=status.HTTP_201_CREATED)
async def create_program(
    program_in: ProgramCreate,
    program_service: ProgramService = Depends(get_program_service),
    current_user: User = Depends(get_current_user),
) -> Program:
    """
    Create a new program.
    The request body should contain the program specifications.
    The user_id will be automatically assigned from the current authenticated user.
    """
    if program_in.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create a program for another user.",
        )

    created_program = await program_service.create_program(program_in)
    return created_program


@router.get("/{program_id}/full/", response_model=Dict[str, Any])
async def get_full_program(
    program_id: str,
    program_service: ProgramService = Depends(get_program_service),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get the full details of a program, including its cycles and workouts.
    """
    details = await program_service.get_full_program_details(program_id)
    if not details or details["program"].user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Program not found"
        )
    return details


@router.put("/{program_id}/adapt/", response_model=Program)
async def adapt_program(
    program_id: str,
    program_update: ProgramUpdate, # Simplified for now
    program_service: ProgramService = Depends(get_program_service),
    current_user: User = Depends(get_current_user),
) -> Program:
    """
    Request a program adaptation.
    For now, this is a simplified update. The full adaptation logic will be
    implemented in the service layer.
    """
    program = await program_service.get_program_by_id(program_id)
    if not program or program.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Program not found"
        )

    updated_program = await program_service.update_program(program_id, program_update)
    if not updated_program:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to adapt program",
        )
    return updated_program
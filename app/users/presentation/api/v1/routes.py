from fastapi import APIRouter
from starlette import status

from app.users.application.dtos import UserReadDTO, UserCreateDTO
from app.users.presentation.api.dependencies import RegisterUCDep

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register/",
    response_model=UserReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "User already exists.",
        },
    },
)
async def register(dto: UserCreateDTO, uc: RegisterUCDep):
    return await uc.execute(dto)

from fastapi import APIRouter
from starlette import status

from app.auth.application.dtos import CredentialsDTO, TokenDTO
from app.auth.presentation.api.dependancies import AuthUCDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token/",
    response_model=TokenDTO,
    summary="Authenticate user with credentials",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
)
async def login(dto: CredentialsDTO, auth_uc: AuthUCDep):
    return await auth_uc.execute(dto)

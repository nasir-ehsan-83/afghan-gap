from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import (
    APIRouter, 
    Depends
)
from src.db.database import get_db
from src.modules.auth.schemas import Token
from src.modules.auth.services import login

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login', response_model = Token)
async def user_login(user_credential: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    # perform login logic in auth_service.py
    return await login(user_credential, db)
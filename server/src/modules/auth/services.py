from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    HTTPException, 
    status
)
from src.modules.users.repository import get_user_by_username
from src.modules.users.model import User
from src.core.jwt import create_access_token
from src.core.security import verify




async def login(user_credential: OAuth2PasswordRequestForm, db: AsyncSession):
    
    user: User = await get_user_by_username(user_credential.username, db)
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Invalid user credential"
        )
    
    # if user.password != user_credetial.password
    if not await verify(user_credential.password, str(user.password)):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Invalid password credential"
        )
    
    access_token = await create_access_token(data = {"user_id" : user.id})

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
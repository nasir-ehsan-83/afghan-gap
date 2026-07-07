from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from fastapi import (
    HTTPException, 
    status
)
from src.modules.users.user_model import User
from src.core.oauth2 import create_access_token
from src.core.security import (
    hash, 
    verify
)

async def login(user_credential: OAuth2PasswordRequestForm, db: AsyncSession):
    
    # get user from database
    user_query = await db.execute(select(User).filter(User.username == user_credential.username))
    user = user_query.scalars().first()

    # if user does not exists
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Invalid user credential"
        )
    
    # else hash the user_credential.password
    password = await hash(user_credential.password)

    # if user.password != user_credetial.password
    if not await verify(user_credential.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Invalid password credential"
        )
    
    access_token = await create_access_token(data = {"user_id" : user.id})

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
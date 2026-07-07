from typing import Dict
from fastapi.concurrency import run_in_threadpool
from jose import (
    jwt, 
    JWTError
)
from datetime import (
    datetime, 
    timedelta
)
from src.tokens.token_schemas import TokenData
from src.config.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

async def create_access_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Use run_in_threadpool for the CPU-bound encoding
    encoded_jwt = await run_in_threadpool(
        jwt.encode, 
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )
    
    return encoded_jwt

async def verify_access_token(token: str, credentials_exception):
    try: 
        # Use run_in_threadpool for the CPU-bound decoding
        payload = await run_in_threadpool(
            jwt.decode, 
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(id=str(user_id))

    except JWTError:
        raise credentials_exception
    
    return token_data

from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status
)
from typing import (
    List, 
    Optional
)
from app.db.database import get_db
from app.dependency.current_user import get_current_user
from app.users.user_model import User
from app.users.user_schema import (
    UserCreate, 
    UserAdminOut, 
    UserPrivateOut,
    UserPublicOut, 
    UserUpdate
)
from app.users.user_service import (
    create_user, 
    get_user_by_email, 
    update_user_by_email, 
    get_user_by_username, 
    get_user_by_id, 
    delete_user_by_email, 
    get_all_users,
    get_users_by_name
)

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

# post user
@router.post('/', response_model = UserPrivateOut)
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await create_user(user_in, db)

# get all user
@router.get('/', response_model = List[UserAdminOut])
async def get_all_user(db: AsyncSession = Depends(get_db)) -> List[User]:
    
    return await get_all_users(db)

# get user by email or username
@router.get('/lookup', response_model = UserPrivateOut)
async def get_user_email(email: Optional[str] = None, username: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    if email:
        return await get_user_by_email(email, db)

    if username:
        return await get_user_by_username(username, db)
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Provide email or username"
    )

# get user by name
@router.get('/search', response_model = List[UserPublicOut])
async def get_user_name(name: str, limit: int = 10, skip: int = 0, db: AsyncSession = Depends(get_db)) -> List[User]:
    return await get_users_by_name(name, limit, skip, db)

# get user by id
@router.get('/id', response_model = UserAdminOut)
async def get_user_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(id, db)

# update user by email
@router.put('/email', response_model=UserPrivateOut)
async def update_user( updated_user: UserUpdate, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    return await update_user_by_email(current_user, updated_user, db)

# delete user by email
@router.delete('/email')
async def delete_user_email(email: str, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    return await delete_user_by_email(email, current_user, db)

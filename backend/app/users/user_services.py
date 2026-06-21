from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update, delete

from app.users.user_schema import UserCreate, UserUpdate
from app.users.user_model import User
from app.core.security import hash

async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
   
    email_query = await db.execute(select(User).filter(User.email == user_in.email))
    if email_query.scalars().first():
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, 
            detail = f"User with email: {user_in.email} already exists"
        )

   
    username_query = await db.execute(select(User).filter(User.username == user_in.username))
    if username_query.scalars().first():
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN, 
            detail = f"User with username: {user_in.username} already exists."
        )
    
    
    user_data = user_in.model_dump()
    user_data["password"] = await hash(user_data["password"])

    new_user = User(**user_data)
    db.add(new_user)
    
    await db.commit() 
    await db.refresh(new_user)
    return new_user

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user_by_email(email: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with email: {email} does not exist!"
        )
    return user

async def get_user_by_username(username: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).filter(func.lower(User.username) == func.lower(username)))
    user = result.scalars().first()
   
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with username: {username} does not exist."
        )
    return user

async def get_users_by_name(name: str, limit: int, skip: int, db: AsyncSession) -> User:
    # get users by name with limit
    user_query = await db.execute(select(User).filter(User.name.contains(name)).limit(limit).offset(skip))
    users = user_query.scalars().all()

    return users

async def get_user_by_id(id: int, db: AsyncSession) -> User:
    result = await db.execute(select(User).filter(User.id == id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User by id: {id} does not exist."
        )
    return user

async def update_user_by_email(updated_user: UserUpdate, current_user: int, db: AsyncSession) -> User:
    # get user from database by email and current id
    result = await db.execute(select(User).filter(User.email == updated_user.email, User.id == int(current_user.id)))
    user = result.scalars().first()

    # if there is not any user by this email
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with email: {updated_user.email} does not exist"
        )
    
    # delete undefined or null elements
    data = updated_user.model_dump(exclude_unset=True)
    
    # if there is a password element then hash it
    if "password" in data:
        data["password"] = await hash(data["password"])
        
    
    for key, value in data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user_by_email(email: str, current_user: int, db: AsyncSession):
    # get user from database at first 
    result = await db.execute(select(User).filter(User.id == int(current_user.id), User.email == email))
    user = result.scalars().first()

    # if there is not any user by this email
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User by emial: {email} does not exist"
        )
    
    # if the user exists then delete this
    await db.delete(user)
    await db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

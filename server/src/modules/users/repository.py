from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import (
    List, 
    Optional
)
from src.modules.users.schemas import (
    UserCreate, 
    UserUpdate
)
from src.modules.users.model import User




async def get_user_by_email(
    email: str, 
    db: AsyncSession
) -> Optional[User]:
    user_query = await db.execute(select(User).filter(User.email == email))

    return user_query.scalars().first()



async def get_user_by_username(
    username: str, 
    db: AsyncSession
) -> Optional[User]:
    user_query = await db.execute(select(User).filter(User.username == username))

    return user_query.scalars().first()



async def create_new_user(
    user_data: UserCreate, 
    db: AsyncSession
) -> User:
    
    new_user = User(**user_data)
    db.add(new_user)
    
    await db.commit() 
    await db.refresh(new_user)

    return new_user


async def get_users(
    db: AsyncSession
) -> List[User]:
    
    users_query = await db.execute(select(User))

    return users_query.scalars().all()



async def get_users_by_name(
    name: str, 
    limit: int, 
    skip: int, 
    db: AsyncSession
) -> List[User]:

    user_query = await db.execute(select(User).filter(User.name.contains(name)).limit(limit).offset(skip))
    
    return user_query.scalars().all()




async def get_user_by_id(
    id: int, 
    db: AsyncSession
) -> User:

    result = await db.execute(select(User).filter(User.id == id))
    
    return result.scalars().first()




async def update_user(
    data: UserUpdate, 
    user: User, 
    db: AsyncSession
) -> User:

    for key, value in data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user




async def delete_user(
    user: User, 
    db: AsyncSession
):

    await db.delete(user)
    await db.commit()

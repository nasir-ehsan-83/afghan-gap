from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import (
    Optional,
    Sequence
)
from src.modules.posts.model import Post
from src.modules.posts.schemas import( 
    PostCreate, 
    PostUpdate
)




async def create_post_db(
    post: PostCreate, 
    owner_id: int, 
    db: AsyncSession
)-> Post:    
    
    new_post = Post(
        owner_id = owner_id, 
        **post.model_dump(exclude_unset = True)
    )
    
    db.add(new_post)

    await db.commit()
    await db.refresh(new_post)

    return new_post




async def get_post_db(
    post_id: int,
    owner_id: int,
    db: AsyncSession
) -> Optional[Post] :
    
    post_query = await db.execute(select(Post).filter(
        Post.id == post_id,
        Post.owner_id = owner_id # type: ignore
    ))
    
    return post_query.scalars().first() 



async def exist_post_db(
    title: str,
    owner_id: int,
    db: AsyncSession
) -> Optional[Post]:
    post_query = await db.execute(select().filter(
        Post.owner_id == owner_id,
        Post.title == title
    ))

    return post_query.scalars().first()
    

async def get_posts_db(
    owner_id: int,
    db: AsyncSession,
    limit: int,
    skip: int,
    title: Optional[str]
) -> Sequence[Post]:
    
    post_query = await db.execute(select(Post).filter(
        Post.owner_id == owner_id, 
        Post.title.contains(title)
    ).limit(limit).offset(skip))
    
    return post_query.scalars().all()



 
async def update_post_db(
    post: Post, 
    update_post: PostUpdate, 
    db: AsyncSession
) -> Post:
    
    data = update_post.model_dump(
        exclude_unset = True, 
        exclude_none = True
    )
    
    for key, value in data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)

    return post




async def delete_post_db(post: Post, db: AsyncSession): 
    
    await db.delete(post)
    await db.commit()
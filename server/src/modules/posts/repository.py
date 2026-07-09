from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import (
    List, 
    Optional
)

from server.src.modules.posts.model import Post
from server.src.modules.posts.schema import PostCreate, PostUpdate




async def create_post(
    post: PostCreate, 
    owner_id: int, 
    db: AsyncSession
)-> Post:    
    # add owner_id to the post details
    new_post = Post(
        owner_id = owner_id, 
        **post.model_dump(exclude_unset = True)
    )
    
    # add new post to DB
    db.add(new_post)

    await db.commit()
    await db.refresh(new_post)

    return new_post




async def get_post (
    post_id: int, 
    owner_id: int, 
    db: AsyncSession
) -> Optional[Post] :
    # get post from DB
    post_query = await db.execute(select(Post).filter(
        Post.id == post_id, 
        Post.owner_id == owner_id
    ))
    
    return post_query.scalars().first() 




# get all posts
async def get_posts(
    owner_id: int,
    db: AsyncSession,
    limit: int,
    skip: int,
    title: str
) -> Optional[List[Post]]:
    # get post from the DB
    post_query = await db.execute(select(Post).filter(
        Post.owner_id == owner_id, 
        Post.title.contains(title)
    ).limit(limit).offset(skip))
    
    return post_query.scalars().all()




# update post    
async def update_post(
    post: Post, 
    update_post: PostUpdate, 
    db: AsyncSession
) -> Post:
    # store updated fields 
    data = update_post.model_dump(
        exclude_unset = True, 
        exclude_none = True
    )
    
    # updated post by updated fields
    for key, value in data.items():
        setattr(post, key, value)

    # save changes
    await db.commit()
    await db.refresh(post)

    return post




# delete post
async def delete_post(post: Post, db: AsyncSession): 
    # delete post from DB
    await db.delete(post)
    await db.commit()
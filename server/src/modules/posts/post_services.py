from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import (
    HTTPException, 
    Response, 
    status
)
from typing import (
    List, 
    Optional
)
from src.modules.posts.post_model import Post
from src.modules.posts.post_schemas import (
    PostCreate, 
    PostUpdate
)

async def create_new_post(post_in: PostCreate, current_user: int, db: AsyncSession,) -> Post:

    new_post = Post(
        owner_id = int(current_user.id), 
        **post_in.model_dump(exclude_unset = True)
    )
    db.add(new_post)

    await db.commit()
    await db.refresh(new_post)

    return new_post

# get a post
async def get_one_post(post_id: int, current_user: int, db: AsyncSession) -> Optional[Post]:

    post_query = await db.execute(select(Post).filter(Post.id == post_id, Post.owner_id == int(current_user.id)))
    post = post_query.scalars().first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with id {current_user.id} does not have the post with id: {post_id}"
        )
    
    return post

# get all posts
async def get_all_posts(current_user: int, db: AsyncSession, limit: int, skip: int, title: str) -> Optional[List[Post]]:

    post_query = await db.execute(select(Post).filter(Post.owner_id == int(current_user.id), Post.title.contains(title)).limit(limit).offset(skip))
    posts = post_query.scalars().all()

    return posts

# update post
async def update_data(post_id: int, update_post: PostUpdate, current_user: int, db: AsyncSession) -> Post:
    
    post_query = await db.execute(select(Post).filter(Post.id == post_id, Post.owner_id == int(current_user.id)))
    post = post_query.scalars().first()

    if not post: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User with id: {current_user.id} does not have the post with id: {post_id}"
        )
    
    data = update_post.model_dump(
        exclude_unset = True, 
        exclude_none = True
    )
    
    for key, value in data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)

    return post

# delete post
async def delete_data(post_id: int, current_user: int, db: AsyncSession) :
    post_query = await db.execute(select(Post).filter(Post.id == post_id, Post.owner_id == int(current_user.id)))
    post = post_query.scalars().first()

    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"User whit id: {current_user.id} does not have the post by id: {post_id}"
        )
    
    await db.delete(post)
    await db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)
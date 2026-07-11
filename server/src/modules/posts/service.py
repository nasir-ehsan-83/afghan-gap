from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
from typing import (
    List, 
    Optional
)
from server.src.modules.posts.repository import (
    create_post,
    delete_post, 
    get_post,
    get_posts
)
from src.modules.posts.model import Post
from src.modules.posts.schema import (
    PostCreate, 
    PostUpdate
)
from src.common.errors import (
    ErrorCode, 
    ConflictException,
    NotFoundException
)




async def create_new_post(
    post: PostCreate, 
    current_user: int, 
    db: AsyncSession
) -> Post:
    # if post already exist
    if await get_post(post.title, current_user.id, db):
        raise ConflictException(
            message = "You already have a post by this name",
            error_code = ErrorCode.POST_ALREADY_EXISTS
        )
    
    # add new post to the DB
    new_post = await create_post(post, current_user.id, db)

    return new_post




# get a post
async def get_one_post(
    post_id: int,
    db: AsyncSession
) -> Optional[Post]:
    # get post from DB
    post = await get_post(post_id, db)

    # if post does not exist
    if not post:
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    return post




# get all posts
async def get_all_posts(
    current_user: int, 
    db: AsyncSession, 
    limit: int, 
    skip: int, 
    title: str
) -> Optional[List[Post]]:

    return await get_posts(current_user.id, db, limit, skip, title)




# update post
async def update_data(
    post_id: int, 
    update_post: PostUpdate, 
    current_user: int, 
    db: AsyncSession
) -> Post:
    # get post from DB 
    post = await get_post(post_id, current_user.id, db)
    
    # if post does not exist
    if not post: 
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    return await update_post(post, update_post, db)




# delete post
async def delete_data(
    post_id: int, 
    current_user: int, 
    db: AsyncSession
) :
    # get post from the DB
    post = await get_post(post_id, current_user.id, db)

    # if post not found
    if not post:
        raise NotFoundException(
            message = "Post Not found",
            error_code = ErrorCode.POST_NOT_FOUND
        )
    
    # delete post from the DB
    await delete_post(post, db)

    return Response(status_code = 204) # HTTP_204_NO_CONTENT
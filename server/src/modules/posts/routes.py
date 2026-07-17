from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter,
    Body, 
    Depends,
    Path,
    Query, 
    status
)
from typing import (
    List, 
    Optional
)
from src.db.database import get_db
from src.common.dependencies.current_user import get_current_user
from src.modules.posts.model import Post
from src.modules.posts.schemas import (
    PostCreate, 
    PostAdminOut, 
    PostPrivateOut, 
    PostPublicOut, 
    PostUpdate
)
from src.modules.posts.services import (
    create_new_post, 
    get_one_post, 
    get_all_posts, 
    update_data, 
    delete_data
)




router = APIRouter(
    prefix = '/api/posts',
    tags = ["Post"]
)

@router.post(
    '/', 
    status_code = status.HTTP_201_CREATED, 
    response_model = PostPrivateOut
)
async def create_post(
    current_user: int = Depends(get_current_user), 
    post: PostCreate = Body(...), 
    db: AsyncSession = Depends(get_db)
) -> Post:

    # send the data to the post_service.py to performe operations 
    return await create_new_post(post, current_user, db)




# get a post of user for admin
@router.get(
    '/{id}', 
    response_model = PostAdminOut
)
async def get_post(
    current_user: int = Depends(get_current_user), 
    id: int = Path(gt = 0), 
    db: AsyncSession = Depends(get_db)
) -> Optional[Post]:

    # send the data to the post_service.py to performe operations 
    return await get_one_post(id, db)




# get all posts for owner
@router.get(
    '/owner', 
    response_model = List[PostAdminOut]
)
async def get_all_posts_admin(
    current_user: int = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db), 
    limit: int = Query(gt = 0), 
    skip: int = Query(gt = 0), 
    search: Optional[str] = Query()
) -> Optional[List[Post]]:

    # send the data to the post_service.py to performe operations 
    return await get_all_posts(current_user, db, limit, skip, search)




# get all posts for all users
@router.get(
    '/search', 
    response_model = List[PostPublicOut]
)
async def get_all_posts_owner(
    current_user = Depends(get_current_user), 
    title: str = Query(), 
    limit: int = Query(gt = 0), 
    skip: int = Query(gt = 0), 
    db: AsyncSession = Depends(get_db)
) -> Optional[List[Post]]:

    # send the data to the post_service.py to performe operations 
    return await get_all_posts(title, current_user, db, limit, skip)




# update post
@router.patch(
    '/{id}', 
    response_model = PostPrivateOut
)
async def update_post(
    current_user = Depends(get_current_user), 
    id: int = Path(gt = 0), 
    update_post: PostUpdate = Body(...), 
    db: AsyncSession = Depends(get_db)
) -> Post:

    # send the data to the post_service.py to performe operations 
    return await update_data(id, update_post, current_user, db)




# delete post
@router.delete(
    '/{id}', 
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete_post(
    current_user = Depends(get_current_user), 
    id: int = Path(gt = 0), 
    db: AsyncSession = Depends(get_db)
) :

    return await delete_data(id, current_user, db)
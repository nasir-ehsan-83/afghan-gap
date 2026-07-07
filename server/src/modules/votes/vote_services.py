from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from fastapi import (
    HTTPException, 
    Response, 
    status
)
from src.modules.votes.vote_model import Vote
from src.modules.posts.post_model import Post
from src.modules.votes.vote_schemas import VoteCreate

async def create_new_vote(vote_in: VoteCreate, owner_id: int, db: AsyncSession) -> Vote:
    # get the post from database
    post_query = await db.execute(select(Post).filter(Post.id == vote_in.post_id))
    existance_post = post_query.scalars().first()

    # if post does not exist
    if not existance_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post with id: {vote_in.id} does not exist"
        )
    
    # get the vote from database
    vote_query = await db.execute(select(Vote).filter(Vote.post_id == vote_in.post_id, Vote.user_id == owner_id))
    found_vote = vote_query.scalars().first()

    # if user want to vote
    if vote_in.vote is True:
        # if user has already voted to the post
        if found_vote:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"Vote already exists"
            )
        
        # else add vote to the database
        vote_data = vote_in.model_dump(exclude_unset = True, exclude_none = False)
        # delete vote.vote from data before storing vote data
        vote_data.pop("vote")
        # add user_id field to the vote data
        vote_data.update({"user_id": owner_id})

        # add new vote
        new_vote = Vote(**vote_data)
        db.add(new_vote)

        await db.commit()
        await db.refresh(new_vote)
        
        return {
            "success": True,
            "message": new_vote
        }
    
    # if user want to devote
    else :
        # if user has not voted yet
        if not found_vote:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Vote does not exist"
            )
        
        # else delete the vote from database
        await db.delete(found_vote)
        await db.commit()

        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
# get all votes of a post
async def get_all_votes(post_id: int, db: AsyncSession) -> List[Vote]:
    # get the post from database
    post_query = await db.execute(select(Post).filter(Post.id == post_id))
    existance_post = post_query.scalars().first()

    # if post does not exits
    if not existance_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Post wit id: {post_id} does not exist"
        )
    
    result = await db.execute(select(Vote).filter(Vote.id == post_id))
    votes = result.scalars().all()

    return votes
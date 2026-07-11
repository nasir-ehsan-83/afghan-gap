from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from src.modules.votes.model import Vote



async def get_vote(
    post_id: int, 
    user_id: int,
    db: AsyncSession
) -> Optional[Vote]:
    
    vote_query = await db.execute(select(Vote).filter(Vote.post_id == post_id, Vote.user_id == user_id))
    
    return vote_query.scalars().first()



async def create_vote(
    vote_data: Vote,
    db: AsyncSession
) -> Vote:
    
    # add new vote
    new_vote = Vote(**vote_data)
    db.add(new_vote)

    await db.commit()
    await db.refresh(new_vote)

    return new_vote



async def get_all_votes(
    post_id: int,
    db: AsyncSession
) -> List[Vote]:
    
    result = await db.execute(select(Vote).filter(Vote.post_id == post_id))
    
    return result.scalars().all()



async def delete_vote(
    vote: Vote,
    db: AsyncSession
):
    
    await db.delete(vote)
    await db.commit()
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import (
    APIRouter, 
    Depends
)
from src.config.database import get_db
from src.modules.votes.vote_model import Vote
from src.modules.votes.vote_schemas import (
    VoteCreate, 
    VoteOut
)
from src.modules.votes.vote_services import (
    create_new_vote, 
    get_all_votes
)

router = APIRouter(
    prefix = "/votes",
    tags = ["Vote"]
)

@router.post('/', response_model = VoteOut)
async def create_vote(vote_in: VoteCreate, owner_id: int, db: AsyncSession = Depends(get_db)) -> Vote:

    return await create_new_vote(vote_in, owner_id, db)

@router.get('/post_id/{post_id}', response_model = List[VoteOut])
async def get_votes(post_id: int, db: AsyncSession = Depends(get_db)) -> List[VoteOut]:

    return await get_all_votes(post_id, db)

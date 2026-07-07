from pydantic import BaseModel, ConfigDict

from src.enums.post import ReactionType

class VoteBase(BaseModel):
    post_id: int
    type: ReactionType

class VoteCreate(VoteBase):
    vote: bool

class VoteOut(VoteBase):
    user_id: int

    model_config = ConfigDict(from_attributes = True)
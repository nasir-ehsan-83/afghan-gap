from sqlalchemy import (
    Column, 
    Integer, 
    ForeignKey, 
    Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from src.config.database import Base
from src.enums.post import ReactionType

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer, 
        ForeignKey("posts.id", ondelete="CASCADE"), 
        primary_key=True
    )
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    type = Column(
        SQLEnum(*(e.value for e in ReactionType), name="reaction_type_enum"), 
        nullable=False
    )

    user = relationship("User")
    post = relationship("Post")

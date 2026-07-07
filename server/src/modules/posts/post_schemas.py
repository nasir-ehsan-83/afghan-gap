from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field
)
from datetime import datetime
from typing import Optional

from src.modules.users.user_schemas import (
    UserAdminOut, 
    UserPrivateOut, 
    UserPublicOut
)

class PostBase(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    content: str = Field(max_length = 250)

class PostCreate(PostBase):
    type: str
    visibility: str
    media_url: str

class PostAdminOut(PostBase):
    id: int
    type: str
    status: str
    visibility: str
    media_url: str
    owner_id: int

    created_at: datetime
    updated_at: datetime
    owner: UserAdminOut

    model_config = ConfigDict(from_attributes = True)

class PostPrivateOut(PostBase):  
    id: int  
    visibility: str
    created_at: datetime
    
    onwer: UserPrivateOut

    model_config = ConfigDict(from_attributes = True)

class PostPublicOut(PostBase):
    owner: UserPublicOut
    pass

    model_config = ConfigDict(from_attributes = True)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(default = None, min_length = 3, max_length = 50)
    content: Optional[str] = Field(default = None, max_length = 250)
    visibility: Optional[str] = None
    media_url: Optional[str] = None
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(min_length = 1, length = 30)
    lastname: Optional[str] = Field(length = 30)
    username: str = Field(min_length=3, max_length=30)
    biography: Optional[str] = Field(max_length = 250)
    email: EmailStr
    visibility: str

    @field_validator("username", "email", mode="before")
    @classmethod
    def normalize_fields(cls, v: str):
        if isinstance(v, str):
            return v.strip().lower()
        return v

# schema for adding new user
class UserCreate(UserBase):
    role: str
    status: str
    password: str = Field(min_length=8)

# schemas's response for admin role
class UserAdminOut(UserBase):
    id: int
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

# schema's response for owner account information
class UserPrivateOut(UserBase):
    id: int
     
    model_config = ConfigDict(from_attributes=True)

# schema's response for all user to see information
class UserPublicOut(BaseModel):
    id: int
    name:str
    lastname: str

    model_config = ConfigDict(from_attributes = True)

class UpdateField(BaseModel):
    name: Optional[str] = Field(None, min_length = 1, max_length = 50)
    lastname: Optional[str] = Field(None, length = 30)
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length = 20)
    biography: Optional[str] = Field(max_length = 250)

    @field_validator("username", "email", mode="before")
    @classmethod
    def normalize_fields(cls, v: str):
        if v is not None and isinstance(v, str):
            return v.strip().lower()
        return v

class UserUpdate(BaseModel):
    email: EmailStr
    update_data: UpdateField
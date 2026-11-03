from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=100)
    role: str = Field(min_length=1, max_length=100)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    """Partial update: fields that are omitted or null are left unchanged."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(default=None, max_length=100)
    role: Optional[str] = Field(default=None, min_length=1, max_length=100)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

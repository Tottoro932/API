from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    username: str
    password_hashed: str
    role: str
    created_at: datetime
    created_by: Optional[int]
    modifed_at: datetime
    modifed_by: Optional[int]

    class Config:
        orm_mode = True

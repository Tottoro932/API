from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TankResponse(BaseModel):
    id: int
    name: str
    max_capacity: float
    current_capacity: float
    product_id: Optional[int]
    created_at: datetime
    created_by: Optional[int]
    modifed_at: datetime
    modifed_by: Optional[int]

    class Config:
        orm_mode = True

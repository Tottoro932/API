from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: Optional[int]
    modifed_at: datetime
    modifed_by: Optional[int]

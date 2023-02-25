from datetime import datetime

from pydantic import BaseModel


class OperationRequest(BaseModel):
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int

from pydantic import BaseModel


class TankRequest(BaseModel):
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int

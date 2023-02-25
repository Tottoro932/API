from pydantic import BaseModel
from datetime import datetime


class FileRequest(BaseModel):
    tank_id: int
    product_id: int
    date_start: datetime
    date_end: datetime

from pydantic import BaseModel


class ProductRequest(BaseModel):
    name: str

from typing import Literal

from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password_text: str
    role: Literal['admin', 'viewer']
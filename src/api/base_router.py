from fastapi import APIRouter

from src.api import tanks
from src.api import products
from src.api import operations
from src.api import users

router = APIRouter()
router.include_router(tanks.router)
router.include_router(products.router)
router.include_router(operations.router)
router.include_router(users.router)
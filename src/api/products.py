from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.models.schemas.products.products_request import ProductRequest
from src.models.schemas.products.products_response import ProductResponse

from src.services.products import ProductsService
from src.services.users import get_current_user_id

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/all', response_model=List[ProductResponse], name='Получить все')
def get(product_service: ProductsService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить данные о всех видах продуктов.
    """
    return product_service.all()


@router.get('/get/{product_id}', response_model=ProductResponse, name='Получить один')
def get(product_id: int, products_service: ProductsService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить данные об одном виде продукта по id.
    """
    return get_with_check(product_id, products_service)


def get_with_check(product_id: int, products_service: ProductsService):
    result = products_service.get(product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Продукт не найден')
    return result


@router.post('/', response_model=ProductResponse, status_code=status.HTTP_201_CREATED, name='Добавить')
def add(
        product_schema: ProductRequest,
        products_service: ProductsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
):
    """
    Добавить данные о продукте.
    """
    return products_service.add(product_schema, called_user_id)


@router.put('/{product_id}', response_model=ProductResponse, name='Обновить')
def put(
        product_id: int,
        product_schema: ProductRequest,
        products_service: ProductsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
):
    """
    Обновить данные об одном типе продукта.
    """
    get_with_check(product_id, products_service)
    return products_service.update(product_id, product_schema, called_user_id)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить')
def delete(
        product_id: int,
        products_service: ProductsService = Depends(),
        called_user_id: int = Depends(get_current_user_id)
):
    """
        Удалить данные о продукте.
    """
    get_with_check(product_id, products_service)
    return products_service.delete(product_id)

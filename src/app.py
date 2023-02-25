from fastapi import FastAPI

from src.api.base_router import router

tags_dict = [
    {
        'name': 'users',
        'description': 'Данные о пользователях',
    },
    {
        'name': 'products',
        'description': 'Данные о продуктах',
    },
    {
        'name': 'tanks',
        'description': 'Данные о резервуарах',
    },
    {
        'name': 'operations',
        'description': 'Данные об операциях',
    }


]


app = FastAPI(
    title='Домашнее задание FastAPI',
    description='Работа с БД',
    version='0.0.1',
    openapi_tags=tags_dict
)

app.include_router(router)

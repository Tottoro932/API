from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.models.schemas.users.users_request import UserRequest
from src.models.schemas.users.users_response import UserResponse
from src.services.users import UsersService
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.users import get_current_user_role, get_current_user_id

router = APIRouter(
    prefix='/users',
    tags=['users']
)


# @router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация')
# def register(user_schema: UserRequest, users_service: UsersService = Depends()):
#     return users_service.register(user_schema)


@router.post('/authorize', response_model=JwtToken, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UsersService = Depends()) -> JwtToken:
    result = users_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован.')
    return result


@router.get('/all', response_model=List[UserResponse], name='Получить все')
def get(user_service: UsersService = Depends(), user_role: str = Depends(get_current_user_role)):
    """
    Получить данные всех пользователей.
    """
    if not user_role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
    return user_service.all()


@router.get('/get/{user_id}', response_model=UserResponse, name='Получить одни')
def get(user_id: int, users_service: UsersService = Depends(), user_role: str = Depends(get_current_user_role)):
    """
    Получить данные одного пользователя по его id.
    """
    if not user_role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
    return get_with_check(user_id, users_service)


def get_with_check(user_id: int, users_service: UsersService):
    result = users_service.get(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    return result


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, name='Добавить')
def add(
        user_schema: UserRequest, users_service: UsersService = Depends(),
        called_user_role: str = Depends(get_current_user_role),
        called_user_id: int = Depends(get_current_user_id)
):
    """
    Добавить данные об одном пользователе по id.
    """
    if not called_user_role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
    return users_service.add(user_schema, called_user_id)


@router.put('/{user_id}', response_model=UserResponse, name='Обновить')
def put(
        user_id: int,
        user_schema: UserRequest,
        users_service: UsersService = Depends(),
        called_user_role: str = Depends(get_current_user_role),
        called_user_id: int = Depends(get_current_user_id)
):
    """
    Обновить данные одного пользователя по id.
    """
    if not called_user_role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
    get_with_check(user_id, users_service)
    return users_service.update(user_id, user_schema, called_user_id)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить')
def delete(user_id: int, users_service: UsersService = Depends(), user_role: str = Depends(get_current_user_role)):
    """
    Удалить данные одного пользователя по id.
    """
    if not user_role == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
    get_with_check(user_id, users_service)
    return users_service.delete(user_id)

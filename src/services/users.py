from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from src.core.settings import settings
from src.db.db import get_session
from src.models.users import Users
from src.models.schemas.users.users_request import UserRequest
from src.models.schemas.utils.jwt_token import JwtToken

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/users/authorize')


def get_current_user_id(token: str = Depends(oauth2_schema)) -> int:
    return UsersService.verify_token(token)


def get_current_user_role(token: str = Depends(oauth2_schema)) -> Optional[int]:
    return UsersService.get_role_av(token)


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password_text: str, password_hashed: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hashed)

    @staticmethod
    def create_token(user_id: int, user_rn: str) -> JwtToken:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id),
            'rn': user_rn
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

        return payload.get('sub')

    #
    @staticmethod
    def get_role_av(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

        return payload.get('rn')

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
                .query(Users)
                .filter(Users.username == username)
                .first()
        )

        if not user:
            return None
        if not self.check_password(password_text, user.password_hashed):
            return None

        return self.create_token(user.id, user.role)

    def all(self) -> List[Users]:
        users = (
            self.session
                .query(Users)
                .order_by(
                Users.id.desc()
            )
                .all()
        )
        return users

    def get(self, user_id: int) -> Users:
        user = (
            self.session
                .query(Users)
                .filter(
                Users.id == user_id
            )
                .first()
        )
        return user

    def add(self, user_schema: UserRequest, created_user_id: int) -> Users:
        datetime_ = datetime.utcnow()
        user = Users(
            username=user_schema.username,
            password_hashed=self.hash_password(user_schema.password_text),
            role=user_schema.role,
            created_at=datetime_,
            created_by=created_user_id,
            modifed_at=datetime_,
            modifed_by=created_user_id
        )
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_schema: UserRequest, modifed_user_id: int) -> Users:
        user = self.get(user_id)
        for field, value in user_schema:
            setattr(user, field, value)
        datetime_ = datetime.utcnow()
        setattr(user, 'modifed_at', datetime_)
        setattr(user, 'modifed_by', modifed_user_id)
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()

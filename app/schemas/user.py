from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема модели пользователя на чтение"""


class UserCreate(schemas.BaseUserCreate):
    """Схема модели пользователя на создание"""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема модели пользователя на обновление"""

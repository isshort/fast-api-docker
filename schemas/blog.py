from pydantic import BaseModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.blog import User as UserModel


class User(BaseModel):
    email: str
    phone: str
    age: int
    password: str

    class Config:
        orm_mode = True


class UserAuthenticateSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserModelSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Album(BaseModel):
    image: str
    user_id: int

    class Config:
        orm_mode = True


class NewsSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True

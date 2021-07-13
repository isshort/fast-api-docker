from pydantic import BaseModel


class User(BaseModel):
    email: str
    phone: str
    age: int
    password:str

    class Config:
        orm_mode = True


class Album(BaseModel):
    image: str
    user_id: int

    class Config:
        orm_mode = True


class News(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True

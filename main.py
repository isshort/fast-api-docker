import os
import uvicorn
from starlette.graphql import GraphQLApp
import graphene
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from phql.blog import (
    CreateUserMutations,

)
from phql.query_data import(
    Query,
)
from models.blog import (
    User,
    Album,
    News
)
from schemas.blog import (
    User as SchemaUser,
    Album as SchemaAlbum,
    News as SchemaNews
)
load_dotenv(".env")

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "Only for checking ok"}


@app.post("/add-user", response_model=SchemaUser)
def add_user(user: SchemaUser):
    db_user = User(email=user.email, phone=user.phone, age=user.age)
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get("/get-user")
def get_user():
    users = db.session.query(User).all()
    return users


@app.post("/add-album", response_model=SchemaAlbum)
def add_album(album: SchemaAlbum):
    db_album = Album(image=album.image, user_id=album.user_id)
    db.session.add(db_album)
    db.session.commit()
    return db_album


@app.get("/get-album")
def get_album():
    return db.session.query(Album).all()


app.add_route("/phql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=CreateUserMutations)))

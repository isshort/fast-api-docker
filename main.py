import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

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

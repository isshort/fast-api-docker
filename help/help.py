import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

load_dotenv(".env")

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']


def create_access_token(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def decode_access_token(data):
    token_data = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
    return token_data

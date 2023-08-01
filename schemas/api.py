# schemas.py

from pydantic import BaseModel


class UserSignup(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Post(BaseModel):
    text: str


class Token(BaseModel):
    access_token: str
    token_type: str

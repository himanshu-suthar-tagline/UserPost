# main.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic
from schemas.api import UserSignup, Post, Token
from typing import Dict
from fastapi import APIRouter
from fastapi import Request
from fastapi import Response
import jwt
from datetime import datetime, timedelta
from config import Settings
from dependencies import get_settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)
security = HTTPBasic()

# In-memory storage for posts
db_posts = {}
users = {
    "john_doe": {
        "password": "password123",  # You should store hashed passwords in a real application
    },
}
post_id_counter = 0


def create_jwt_token(
    data: dict, settings, expires_delta: timedelta = timedelta(minutes=15)
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_jwt_token(token: str, settings):
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_current_user(request: Request, settings: Settings = Depends(get_settings)):
    token = request.cookies.get("access_token")

    token_data = decode_jwt_token(token, settings)
    print(token_data)
    if token_data.sub not in users:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": token.username}


@router.post("/signup", response_model=Token)
async def signup(
    user: UserSignup,
    request: Request,
    settings: Settings = Depends(get_settings),
):
    if users.get(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    # You should store the hashed password in a real application
    users[user.username] = {"password": user.password}
    access_token = create_jwt_token({"sub": user.username}, settings=settings)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(
    user: UserSignup,
    response: Response,
    settings: Settings = Depends(get_settings),
):
    user_data = users.get(user.username)
    if not user_data or user.password != user_data["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = create_jwt_token({"sub": user.username}, settings=settings)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/addPost", response_model=str)
async def add_post(post: Post, user=Depends(get_current_user)):
    global post_id_counter
    post_id_counter += 1
    post_id = str(post_id_counter)
    db_posts[post_id] = {"text": post.text, "username": user["username"]}
    return post_id


@router.get("/getPosts", response_model=Dict[str, str])
async def get_posts(user: Dict[str, str] = Depends(get_current_user)):
    user_posts = {
        post_id: post["text"]
        for post_id, post in db_posts.items()
        if post["username"] == user["username"]
    }
    return user_posts

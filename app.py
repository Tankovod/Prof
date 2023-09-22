from datetime import datetime, timedelta
from typing import Annotated
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, templates
from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from src.types_.types__ import Token, User
from src.dependencies import get_current_active_user
from src.utils.jwt_auth import authenticate_user, create_access_token
from fastapi.staticfiles import StaticFiles
from src.database.db_func import post_user
from src.api.router import router as api_router
from src.drova.router import router as views_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, **{'allow_methods': ('*',), 'allow_origins': ('*',), 'allow_headers': ('*',), })
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=api_router)
app.include_router(router=views_router)


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, get_current_active_user]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[User, get_current_active_user]
):
    return [{"item_id": "Foo", "owner": current_user.phone}]


@app.get("/index")
async def root():
    return {"message": "Hello World"}






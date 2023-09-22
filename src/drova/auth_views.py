from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Request, Depends, status, HTTPException
from starlette.responses import HTMLResponse

from src.database.models import Product
from src.dependencies import get_current_active_user
from src.settings import templates, ACCESS_TOKEN_EXPIRE_MINUTES
from src.types_.types__ import User, Token
from src.utils.jwt_auth import authenticate_user, create_access_token

router = APIRouter(
    prefix='/auth',
    default_response_class=HTMLResponse,
    include_in_schema=False
)


@router.post(path="/registration")
async def sign_up_post(request: Request):
    return templates.TemplateResponse('main/auth/registration.html', context={"request": request})


@router.get(path="/registration")
async def sign_up_get(request: Request):
    return templates.TemplateResponse('main/auth/registration.html', context={"request": request})


@router.get(path="/login")
async def sign_up_get(request: Request):
    return templates.TemplateResponse('main/auth/login.html', context={"request": request})


@router.post(path="/login")
async def sign_up_get(request: Request,  form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
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
    return templates.TemplateResponse('main/auth/login.html', context={"request": request,
                                                                       "access_token": access_token, "token_type": "bearer"})
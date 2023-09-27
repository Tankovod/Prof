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
app.add_middleware(CORSMiddleware, allow_credentials=True,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',), 'allow_headers': ('*',), })
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=api_router)
app.include_router(router=views_router)


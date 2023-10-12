from datetime import timedelta
from src.validation.settings import settings
import sqlalchemy.exc
import ulid
from fastapi import APIRouter, Request, Form, BackgroundTasks, status
from fastapi.responses import RedirectResponse
from src.database.db_func import get_user
from src.utils.jwt_auth import get_password_hash, token_check
from src.database.models import UserSite
from src.validation.user_validators import User
from src.validation.auth_validators import LoginData
from src.utils.jwt_auth import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['Auth'])


async def save_user(form: UserSite):
    form.password = await get_password_hash(form.password)
    async with UserSite.async_session() as session:
        async with session.begin():
            session.add(form)
            # session.expunge_all()


@router.post(path="/registration",
             status_code=status.HTTP_201_CREATED,
             response_model_exclude={'password'},
             name="New user sign up")
async def sign_up(form: User):
    print(form.phone, form.password)
    user_id = ulid.ulid()
    form = UserSite(id=user_id, **form.model_dump())
    try:
        await save_user(form=form)
    except sqlalchemy.exc.IntegrityError as ex:
        message = 'Данный email или номер телефона уже зарегистрированы'
        token, http_response = '', status.HTTP_401_UNAUTHORIZED
    else:
        message = "Вы зарегистрированы!"
        token = await create_access_token(data={"sub": user_id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        http_response = status.HTTP_201_CREATED

    response = {'message': message, 'token': token, 'HTTP_response': http_response, **form.__dict__}
    return response


@router.post(path="/login")
async def sign_in(form: LoginData) -> dict:
    current_user = await get_user(phone=form.phone)
    if current_user and await verify_password(plain_password=form.password, hashed_password=current_user.password):
        token = await create_access_token(data={"sub": current_user.id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {'token': token}
    else:
        return {'message': 'Неверный логин и(или) пароль'}


@router.post(path="/token")
async def validate_token(token: dict) -> None | int:
    return await token_check(token=token['access_token'].split('=')[1])

from datetime import timedelta

import sqlalchemy.exc
import ulid
from fastapi import APIRouter, Request, Form, BackgroundTasks, status
from src.utils.jwt_auth import get_password_hash, token_check
from src.database.models import UserSite
from src.types_.types__ import User
from src.utils.jwt_auth import create_access_token

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
async def sign_up(
        form: User):
    user_id = ulid.ulid()
    form = UserSite(id=user_id, **form.model_dump())
    try:
        await save_user(form=form)
    except sqlalchemy.exc.IntegrityError as ex:
        message = 'Данный email или номер телефона уже зарегистрированы'
        token, http_response = '', 401
    else:
        message = "Вы зарегистрированы!"
        token = await create_access_token(data={"sub": user_id}, expires_delta=timedelta(minutes=2))
        http_response = 201

    response = {'message': message, 'token': token, 'HTTP_response': http_response, **form.__dict__}
    return response


@router.post(path="/token")
async def validate_token(token: dict):
    return await token_check(token=token['access_token'])

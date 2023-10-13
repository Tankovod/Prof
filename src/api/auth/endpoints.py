from datetime import timedelta
from fastapi.responses import ORJSONResponse
from .router import router
from src.validation.settings import settings
import sqlalchemy.exc
from fastapi import status
from src.database.db_func import get_user
from src.utils.jwt_auth import get_password_hash, token_check
from src.database.models import UserSite
from src.validation.user_validators import User
from src.validation.auth_validators import LoginData
from src.utils.jwt_auth import create_access_token, verify_password


@router.post(path="/registration",
             status_code=status.HTTP_201_CREATED,
             response_model_exclude={'password'},
             name="New user sign up")
async def sign_up(form: User) -> ORJSONResponse:
    user = UserSite(**form.model_dump())
    try:
        user.password = await get_password_hash(user.password)
        async with UserSite.async_session() as session:
            async with session.begin():
                session.add(user)
                session.commit()

    except sqlalchemy.exc.IntegrityError as ex:
        message = 'Данный email или номер телефона уже зарегистрированы'
        token, status_code = '', status.HTTP_401_UNAUTHORIZED

    else:
        message = "Вы зарегистрированы!"
        token = await create_access_token(data={"sub": form.id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        status_code = status.HTTP_201_CREATED

    return ORJSONResponse(content={'message': message, 'token': token, **form.model_dump(
        exclude={"password", "disabled"})}, status_code=status_code)


@router.post(path="/login")
async def sign_in(form: LoginData) -> ORJSONResponse:
    current_user = await get_user(phone=form.phone)
    if current_user and await verify_password(plain_password=form.password, hashed_password=current_user.password):
        token = await create_access_token(data={"sub": current_user.id},
                                          expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return ORJSONResponse(content={'token': token}, status_code=status.HTTP_200_OK)
    else:
        return ORJSONResponse(content={'message': 'Неверный логин и(или) пароль'},
                              status_code=status.HTTP_400_BAD_REQUEST)


@router.post(path="/token")
async def validate_token(token: dict) -> None | int:
    return await token_check(token=token['access_token'].split('=')[1])

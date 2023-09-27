from functools import wraps

from sqlalchemy import select

from src.database.db_func import get_user
from src.types_.types__ import ProductValid
from src.utils.jwt_auth import token_check, get_user_id
from fastapi import APIRouter, Request, Depends, Response, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from starlette.responses import HTMLResponse
from src.database.models import Product, UserSite
from src.settings import templates

router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)


def auth_required(func):
    @wraps(func)
    async def wrapper(request: Request):
        if 'access_token' in request.cookies:
            if await token_check(request.cookies['access_token']) == status.HTTP_401_UNAUTHORIZED:
                return RedirectResponse("/auth/login", status_code=status.HTTP_401_UNAUTHORIZED)
            return await func(request)
        else:
            return RedirectResponse("/auth/login")

    return wrapper


@router.get(path="/add_product")
@auth_required
async def get_product(request: Request):
    product_columns = [(i.name, i.doc) for i in [*Product.metadata.tables.get('product').columns] if
                       i.name not in ['id', 'actual_date']]
    return templates.TemplateResponse('main/product/add_product.html',
                                      context={"request": request, "product": product_columns, "is_auth": True})


@router.get(path="/profile")
@auth_required
async def get_user_profile(request: Request):
    user_id = await get_user_id(request.cookies['access_token'])
    user = await get_user(user_id=user_id)
    user.password = None
    return templates.TemplateResponse('main/profile.html', context={"request": request, "user": user, "is_auth": True})


@router.get("/")
async def get_home(request: Request):
    is_auth = False
    if 'access_token' in request.cookies: is_auth = True
    async with Product.async_session() as session:
        products = await session.scalars(select(Product))
    return templates.TemplateResponse('main/home.html', context={"request": request, "products": products,
                                                                 "is_auth": is_auth})

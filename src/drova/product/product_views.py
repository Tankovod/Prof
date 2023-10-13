from functools import wraps

from fastapi import Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from src.database.models import Product
from src.dependencies import is_user_authorized, user_auth_views
from src.settings import templates
from src.tasks import celery_newsletter
from src.utils.jwt_auth import token_check
from src.validation.user_validators import UserView
from .router import router


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
async def get_product(request: Request, user: UserView = user_auth_views):
    product_columns = [(i.name, i.doc) for i in [*Product.metadata.tables.get('').columns] if
                       i.name not in ['id', 'actual_date']]
    return templates.TemplateResponse('main/product/add_product.html',
                                      context={"request": request, "product": product_columns, "user": user})


@router.get(path="/profile")
async def get_user_profile(request: Request, user: UserView = user_auth_views):
    return templates.TemplateResponse('main/profile.html', context={"request": request, "user": user})


@router.get("/")
async def get_home(request: Request, user: UserView | None = is_user_authorized):
    d = celery_newsletter.delay()

    async with Product.async_session() as session:
        products = await session.scalars(select(Product))
    return templates.TemplateResponse('main/index.html', context={"request": request, "products": products,
                                                                  "user": user})

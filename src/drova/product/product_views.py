from functools import wraps

from fastapi import Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from src.database.models import Product, ProductUnit
from src.dependencies import is_user_authorized, user_auth_views
from src.settings import templates
from src.tasks import celery_newsletter
from src.utils.jwt_auth import token_check
from src.validation.user_validators import UserView
from .router import router
from ...database.base import Base


async def get_table_columns(table_model, table_name: str, exclude: list[str]) -> list[tuple[str, str]]:
    return [(i.name, i.doc) for i in [*table_model.metadata.tables.get(table_name).columns] if
            i.name not in exclude]


@router.get(path="/add_product")
async def get_product(request: Request, user: UserView = user_auth_views):
    product_columns = await get_table_columns(table_model=Product, table_name="product",
                                              exclude=['id', 'actual_date', 'is_new', 'unit_id', 'slug'])
    async with ProductUnit.async_session() as session:
        units = await session.execute(select(ProductUnit))
        units = [*units.scalars()]
    return templates.TemplateResponse('main/product/add_product.html', context={"request": request, "product":
        product_columns, "units": units, "user": user})


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

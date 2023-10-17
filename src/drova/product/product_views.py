from typing import Union, Optional

from fastapi import Request, status
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import selectinload

from src.database.models import Product, ProductUnit, ProductImage
from src.dependencies import is_user_authorized, user_auth_views
from src.settings import templates
from src.validation.user_validators import UserView
from .router import router


async def get_table_columns(table_model, table_name: str, exclude: list[str]) -> list[tuple[str, str]]:
    return [(i.name, i.doc) for i in [*table_model.metadata.tables.get(table_name).columns] if
            i.name not in exclude]


@router.get(path="/add-product")
async def get_product(request: Request, user_or_401: Union[UserView, status] = user_auth_views):
    if user_or_401 == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_401_UNAUTHORIZED)
    product_columns = await get_table_columns(table_model=Product, table_name="product",
                                              exclude=['id', 'actual_date', 'is_new', 'unit_id', 'slug'])
    async with ProductUnit.async_session() as session:
        units = await session.execute(select(ProductUnit))
        units = [*units.scalars()]
    return templates.TemplateResponse('main/product/add_product.html', context={"request": request, "product":
        product_columns, "units": units, "user": user_or_401})


@router.get(path="/profile")
async def get_user_profile(request: Request, user: UserView = user_auth_views):
    return templates.TemplateResponse('main/profile.html', context={"request": request, "user": user})


@router.get("/")
async def get_home(request: Request, user_or_401: Union[UserView, status] = is_user_authorized):
    async with Product.async_session() as session:
        products = await session.scalars(select(Product).options(selectinload(Product.images), selectinload(Product.units)))
        # print([(i.images, i.units) for i in [*products]])
        # products = [*products]
        # print(products)
    return templates.TemplateResponse('main/index.html', context={"request": request, "products": products,
                                                                  "user": user_or_401})

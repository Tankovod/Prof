import datetime
from fastapi import status, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.validation.product_validators import ProductValid, ProductModelDb
from .router import router
from src.database.models import Product, ProductImage
from sqlalchemy.exc import IntegrityError
from src.dependencies import user_auth_api, get_product_info
from ...validation.user_validators import UserView


@router.post(path="/add-product",
             name="Add new product",
             status_code=status.HTTP_201_CREATED,
             response_model=ProductValid
             )
async def add_product(form: ProductValid, user: UserView = user_auth_api) -> ProductValid:
    async with Product.async_session() as session:
        async with session.begin():
            product = Product(**form.model_dump(exclude={"images"}), images=[
                ProductImage(image_link=link) for link in form.images], actual_date=datetime.datetime.now())
            session.add(product)
            try:
                await session.commit()
            except IntegrityError:
                raise HTTPException(detail="Similar product is already exists", status_code=status.HTTP_400_BAD_REQUEST)
            session.refresh(product)
    return form


@router.get(path="/products",
            name="Get all products",
            status_code=status.HTTP_200_OK,
            response_model=list[ProductValid])
async def get_all_products() -> list[ProductModelDb]:
    async with Product.async_session() as session:
        products = await session.scalars(select(Product).options(selectinload(Product.images), selectinload(Product.units)))
    return [ProductModelDb.model_validate(obj=product, from_attributes=True) for product in products]


@router.get(path="/products/{slug}",
            name="Get product's info",
            status_code=status.HTTP_200_OK,
            response_model=ProductValid)
async def get_product_info(product: Product = get_product_info) -> ProductValid:
    return ProductValid.model_validate(obj=product, from_attributes=True)

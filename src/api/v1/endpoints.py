import datetime
from fastapi import status, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select

from src.validation.product_validators import ProductValid
from .router import router
from src.database.models import Product
from sqlalchemy.exc import IntegrityError
from src.dependencies import user_auth_api, get_product_info
from ...validation.user_validators import UserView


@router.post(path="/add-product",
             name="Add new product",
             status_code=status.HTTP_201_CREATED,
             )
async def add_product(form: ProductValid, user: UserView = user_auth_api) -> ORJSONResponse:
    async with Product.async_session() as session:
        async with session.begin():
            product = Product(**form.model_dump(), actual_date=datetime.datetime.now())
            session.add(product)
            try:
                await session.commit()
            except IntegrityError:
                raise HTTPException(detail="Similar product is already exists", status_code=status.HTTP_400_BAD_REQUEST)
            session.refresh(product)
    return ORJSONResponse(content={**form.model_dump()},
                          status_code=status.HTTP_201_CREATED)


@router.get(path="/products", name="Get all products", status_code=status.HTTP_200_OK)
async def get_all_products() -> ORJSONResponse:
    async with Product.async_session() as session:
        products = await session.execute(select(Product))
    return ORJSONResponse(content=[*products.scalars()], status_code=status.HTTP_200_OK)


@router.get(path="/products/{slug}", name="Get product's info", status_code=status.HTTP_200_OK)
async def get_product_info(product: Product = get_product_info) -> ProductValid:
    return ProductValid.model_validate(obj=product, from_attributes=True)

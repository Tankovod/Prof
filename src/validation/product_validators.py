from pydantic import BaseModel, Field, PositiveFloat, model_validator, PositiveInt, BaseConfig
from typing import Optional
from typing_extensions import Self
from slugify import slugify

from src.database.models import ProductImage, ProductUnit


class ProductModel(BaseModel):
    title: str = Field(default=..., min_length=3, max_length=64, title="Product name")
    slug: str = Field(default=..., min_length=3, max_length=64, title="Product slug")
    description: Optional[str] = ...
    amount: PositiveFloat = Field(default=..., gt=0, title="Amount of product")
    unit_id: PositiveInt
    is_new: bool = Field(default=True)


class ProductValid(ProductModel):
    images: Optional[list[str]] = Field(
        default=["https://images.assetsdelivery.com/compings_v2/yehorlisnyi/yehorlisnyi2104/yehorlisnyi210400016.jpg"],
        title="Product's images")

    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.get("slug") is None:
            self["slug"] = slugify(self["title"])
        return self


class FModel(BaseModel):
    id: PositiveInt

    class Config:
        from_attributes = True


class UnitModelDb(FModel):
    name: str


class ImageModelDb(FModel):
    product_id: PositiveInt
    image_link: str


class ProductModelDb(ProductModel, FModel):
    images: list[ImageModelDb]
    units: UnitModelDb

    class Config:
        from_attributes = True

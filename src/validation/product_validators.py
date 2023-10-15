from pydantic import BaseModel, Field, PositiveFloat, model_validator, PositiveInt
from typing import Optional
from typing_extensions import Self
from slugify import slugify


class ProductValid(BaseModel):
    title: str = Field(default=..., min_length=3, max_length=64, title="Product name")
    slug: str = Field(default=..., min_length=3, max_length=64, title="Product slug")
    description: Optional[str] = ...
    amount: PositiveFloat = Field(default=..., gt=0, title="Amount of product")
    unit_id: PositiveInt
    images: Optional[list[str]] = Field(
        default=["https://images.assetsdelivery.com/compings_v2/yehorlisnyi/yehorlisnyi2104/yehorlisnyi210400016.jpg"],
        title="Product's images")
    is_new: bool = Field(default=True)

    @model_validator(mode='before')
    def validator(self) -> Self:
        if self.get("slug") is None:
            self["slug"] = slugify(self["title"])
        return self

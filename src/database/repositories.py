from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, async_session

from .models import Product, ProductUnit, ProductImage, UserSite
from ..dependencies import get_session


class Specification:
    async def is_satisfied(self):
        raise NotImplementedError()


class ProductSpecification(Specification):
    def __init__(self, slug):
        self.slug = slug

    async def is_satisfied(self) -> dict:
        return {"slug": self.slug}


class BaseRepository:
    def __init__(self, model):
        self._model = model

    async def get(self, specification: Specification, session: async_session = get_session):
        return await session.scalar(select(self._model).filter(*await specification.is_satisfied()))


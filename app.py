from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.router import router as api_router
from src.database.base import Base
from src.drova.router import router as views_router
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from src.database.models import UserSite, Product, ProductUnit, ProductImage


app = FastAPI()
app.add_middleware(CORSMiddleware,
                   **{'allow_methods': ('*',), 'allow_origins': ('*',),
                      'allow_headers': ('*',), 'allow_credentials': True})
app.mount("/static", StaticFiles(directory="static/main"), name="static")
app.include_router(router=api_router)
app.include_router(router=views_router)

# ----------   SQLAdmin ----------------
admin = Admin(app=app, engine=Base.async_engine)


class UserAdmin(ModelView, model=UserSite):
    column_list = [UserSite.email, UserSite.phone, UserSite.first_name, UserSite.last_name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.title, Product.amount, Product.is_new, Product.unit_id]


class UnitAdmin(ModelView, model=ProductUnit):
    column_list = [ProductUnit.name, ProductUnit.products]


admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
admin.add_view(UnitAdmin)

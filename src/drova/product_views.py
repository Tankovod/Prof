from functools import wraps

from fastapi import APIRouter, Request, Depends
from starlette.responses import HTMLResponse
from src.database.models import Product
from src.settings import templates


router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper

async def verify_token():
    

@router.get(path="/add_product")
async def get_product(request: Request, dependencies=[Depends(verify_token), Depends(verify_key)]):
    product_columns = [(i.name, i.doc) for i in [*Product.metadata.tables.get('product').columns] if i.name not in ['id','actual_date']]
    return templates.TemplateResponse('main/product/add_product.html', context={"request": request, "product": product_columns})
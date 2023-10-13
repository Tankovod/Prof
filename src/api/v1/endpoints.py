import datetime

from .router import router
from src.database.models import Product


@router.post(path="/add_product")
async def get_product(form: dict):
    async with Product.async_session() as session:
        async with session.begin():
            product = Product(title=form['title'], description=form['description'],
                              units=form['units'], amount=int(form['amount']), actual_date=datetime.datetime.now())
            session.add(product)
            session.commit()
            session.refresh(product)

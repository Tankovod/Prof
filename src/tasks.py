import asyncio

from src.database.models import Product
from src.settings import celery
from src.database.db_func import select_emails, select_new_products
from src.utils.send_email import make_email_template, send_template


@celery.task()
def celery_newsletter() -> None:
    async def send_data_to_emails() -> None:
        products = await select_new_products()
        if products:
            emails = await select_emails()
            for email in emails:
                template = await make_email_template(target_email=email, new_products=products)
                await send_template(template=template)
            for product in products:  # products are shown
                product.is_new = False
            async with Product.async_session() as session:  # update new products
                session.add_all(products)
                await session.commit()

    loop = asyncio.get_event_loop()
    cor = send_data_to_emails()
    loop.run_until_complete(cor)

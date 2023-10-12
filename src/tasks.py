import asyncio
from src.settings import celery
from src.database.db_func import select_emails, select_new_products
from src.utils.send_email import make_email_template, send_template


@celery.task()
def celery_newsletter():
    async def send_data_to_emails() -> None:
        emails = await select_emails()
        print([*emails])
        products = await select_new_products()
        print(products)
        for email in emails:
            template = await make_email_template(target_email=email, new_products=products)
            await send_template(template=template)
            print(template)

    print(34534342432)
    loop = asyncio.get_event_loop()
    cor = send_data_to_emails()
    loop.run_until_complete(cor)

from email.message import EmailMessage
import smtplib
from src.database.models import Product
from src.validation.smtp_settings import smtp_settings


async def make_email_template(target_email: str, new_products: list[Product]) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Новые поступления в магазин'
    email['From'] = smtp_settings.SMTP_USER
    email['To'] = target_email

    content = "\n".join([f"{product.title} в количестве {product.amount} {product}"
                         for product in new_products])

    email.set_content(
        f'''<div>
        {content}
        </div>,
        subtype=html'''
    )
    return email


async def send_template(template: EmailMessage) -> None:
    with smtplib.SMTP_SSL(host=smtp_settings.SMTP_HOST, port=smtp_settings.SMTP_PORT) as server:
        server.login(user=smtp_settings.SMTP_USER, password=smtp_settings.SMTP_PASS)
        server.send_message(msg=template)


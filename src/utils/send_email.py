from email.message import EmailMessage
import smtplib
from src.validation.smtp_settings import SMTPSettings
from src.database.models import Product
from src.validation.settings import settings


async def make_email_template(target_email: str, new_products: list[Product]) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Новые поступления в магазин'
    email['From'] = settings.SMTP_USER
    email['To'] = target_email

    content = "\n".join([f"{product.title} в количестве {product.amount} {product}:\n Фото товара: {product.images[0]}"
                         for product in new_products])

    email.set_content(
        f'''<div>
        {content}
        </div>,
        subtype=html'''
    )
    return email


async def send_template(template: EmailMessage) -> None:
    with smtplib.SMTP_SSL(host=SMTPSettings.SMTP_HOST, port=SMTPSettings.SMTP_PORT) as server:
        server.login(user=SMTPSettings.SMTP_USER, password=SMTPSettings.SMTP_PASS)
        server.send_message(msg=template)


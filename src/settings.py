from pathlib import Path
from celery import Celery
from redis import Redis
from src.validation.settings import settings
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

celery = Celery()
celery.config_from_object(obj=settings, namespace='CELERY')
celery.autodiscover_tasks(packages=['src'])
redis = Redis.from_url(url=settings.REDIS_URL.unicode_string())  # ???

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory="templates")

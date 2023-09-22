from pathlib import Path

from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
BASE_DIR = Path(__file__).resolve().parent.parent
ACCESS_TOKEN_EXPIRE_MINUTES = 1320
templates = Jinja2Templates(directory="templates")

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter(
    prefix='/auth', tags=['Auth'],
)


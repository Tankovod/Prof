from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter(
    prefix='/v1',
    default_response_class=ORJSONResponse
)

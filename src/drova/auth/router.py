from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/auth',
    default_response_class=HTMLResponse,
    include_in_schema=False
)
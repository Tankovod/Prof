from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from src.settings import templates

router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)


@router.post(path="/registration")
async def sign_up_post(request: Request):
    return templates.TemplateResponse('main/registration.html', context={"request": request})


@router.get(path="/registration")
async def sign_up_get(request: Request):
    return templates.TemplateResponse('main/registration.html', context={"request": request})

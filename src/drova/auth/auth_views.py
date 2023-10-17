from fastapi import Request, status
from fastapi.responses import RedirectResponse

from src.settings import templates
from src.utils.jwt_auth import token_check
from .router import router


async def dont_show_auth(request: Request):
    if 'access_token' in request.cookies:
        return await token_check(request.cookies['access_token'])
    else:
        return status.HTTP_401_UNAUTHORIZED


@router.get(path="/registration")
async def sign_up_get(request: Request):
    if await dont_show_auth(request=request) == status.HTTP_401_UNAUTHORIZED:
        return templates.TemplateResponse('main/auth/registration.html', context={"request": request})
    else:
        return RedirectResponse(url="/")


@router.get(path="/login")
async def sign_up_get(request: Request):
    if await dont_show_auth(request=request) == status.HTTP_401_UNAUTHORIZED:
        return templates.TemplateResponse('main/auth/login.html', context={"request": request})
    else:
        return RedirectResponse(url="/")

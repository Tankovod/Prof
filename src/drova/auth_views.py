from fastapi import APIRouter, Request, Depends, status, HTTPException
from starlette.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from src.settings import templates
from src.utils.jwt_auth import authenticate_user, create_access_token, token_check


router = APIRouter(
    prefix='/auth',
    default_response_class=HTMLResponse,
    include_in_schema=False
)


async def dont_show_auth(request: Request):
    # print(request.cookies)
    if 'access_token' in request.cookies:
        if await token_check(request.cookies['access_token']) == status.HTTP_401_UNAUTHORIZED:
            return status.HTTP_401_UNAUTHORIZED
    else:
        return status.HTTP_401_UNAUTHORIZED


@router.get(path="/registration")
async def sign_up_get(request: Request):
    # print([*dict(request).items()])
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

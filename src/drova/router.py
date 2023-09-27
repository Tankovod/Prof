from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from starlette.responses import HTMLResponse
from .product_views import router as product_router
from .auth_views import router as auth_router

router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)
router.include_router(router=auth_router)
router.include_router(router=product_router)


from fastapi import APIRouter
from starlette.responses import HTMLResponse
from src.drova.product.product_views import router as product_router
from src.drova.auth.auth_views import router as auth_router

router = APIRouter(
    default_response_class=HTMLResponse,
    include_in_schema=False
)
router.include_router(router=auth_router)
router.include_router(router=product_router)


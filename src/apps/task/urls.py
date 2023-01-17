from src.apps.task.app import APP
from src.apps.task.api.coupon.views import router as coupon_router

APP.include_router(coupon_router, prefix='/api/coupon')

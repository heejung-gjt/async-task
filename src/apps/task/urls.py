from apps.task.app import APP
from apps.task.api.coupon.views import router as coupon_router

APP.include_router(coupon_router, prefix='/api/coupon')

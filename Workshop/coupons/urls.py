from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^apply/$',
        views.coupon_apply,
        name="coupon_apply"),
    url(r'^register/$',
        views.register_new_coupon,
        name="coupon_register"),
]

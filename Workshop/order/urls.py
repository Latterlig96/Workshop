from django.urls import path
from . import views


urlpatterns = [
    path('order/link/<int:id>/success',
         views.send_payment_link,
         name="payment_link_send")
]

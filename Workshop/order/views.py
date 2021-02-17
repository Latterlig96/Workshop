from http import HTTPStatus
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import OrderInformation


@permission_required('shop.can_resolve_order')
def send_payment_link(request: WSGIRequest,
                      id: int) -> HttpResponse:
    order_info = OrderInformation.objects.get(id=id)
    template = render_to_string('order/order_payment_link.html',
                                context={'name': order_info.name,
                                         'surname': order_info.surname})
    email = EmailMessage(
        'Payment Link',
        template,
        settings.EMAIL_HOST_USER,
        [order_info.email])
    email.fail_silently = False
    email.send()

    return render(request,
                  'order/order_link_sent_success.html',
                  {'order': order_info},
                  status=HTTPStatus.OK)

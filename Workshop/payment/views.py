import braintree
from django.shortcuts import render, redirect
from django.conf import settings
from order.models import OrderInformation, OrderItem
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from http import HTTPStatus

def payment_process(request: WSGIRequest,
                    id: int
                    ) -> HttpResponse:
    gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)
    order_info = OrderInformation.objects.get(id=id)
    order_items = OrderItem.objects.filter(order_information=order_info).all()
    total_cost = sum(order_item.get_total_cost for order_item in order_items)
    if request.method == "POST":
        nonce = request.POST.get('payment_method_nonce',
                                 None)
        result = gateway.transaction.sale({
            'amount': f"{total_cost:.2f}",
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success: 
            order_info.paid = True
            order_info.braintree_id = result.transaction.id
            order_info.save()
            return redirect('payment_done') 
        return redirect('payment_canceled')
    else: 
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order_info,
                       'item': order_items,
                       'client_token': client_token},
                       status=HTTPStatus.OK)

def payment_done(request: WSGIRequest) -> HttpResponse:
    return render(request, 
                  'payment/done.html',
                  status=HTTPStatus.OK)

def payment_canceled(request: WSGIRequest) -> HttpResponse:
    return render(request, 
                  'payment/canceled.html',
                  status=HTTPStatus.OK)

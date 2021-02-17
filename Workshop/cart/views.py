from http import HTTPStatus
from typing import Dict
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request: WSGIRequest,
             product_id: int
             ) -> HttpResponse:
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd: Dict = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request: WSGIRequest,
                product_id: int
                ) -> HttpResponse:
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request: WSGIRequest) -> HttpResponse:
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'cart/cart_detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form},
                  status=HTTPStatus.OK)

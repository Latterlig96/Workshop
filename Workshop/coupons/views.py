from typing import Dict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import CouponApplyForm, CouponRegister
from .models import Coupon
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone
from http import HTTPStatus


@require_POST
def coupon_apply(request: WSGIRequest) -> HttpResponse:
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart_detail')

@login_required 
@permission_required('shop.can_create_coupons')
def register_new_coupon(request: WSGIRequest) -> HttpResponse: 
    if request.method == "POST": 
        coupon_form = CouponRegister(request.POST)
        if coupon_form.is_valid(): 
            cd: Dict = coupon_form.cleaned_data
            Coupon.objects.create(code=cd['code'],
                                  valid_from=cd['valid_from'],
                                  valid_to=cd['valid_to'],
                                  discount=cd['discount'],
                                  active=cd['active'])
            messages.success(request, "Coupon created sucessfully")
            return redirect('owner_dashboard')
    else: 
        coupon_form = CouponRegister()
        return render(request,
                      'shop/owner/register_coupon.html',
                      {'form': coupon_form},
                      status=HTTPStatus.OK)

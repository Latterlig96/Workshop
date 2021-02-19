from django import forms
from .models import Coupon

class CouponApplyForm(forms.Form): 
    code = forms.CharField()

class CouponRegister(forms.Form): 
    class Meta: 
        model = Coupon
        fields = '__all__'

from django.db import models
from shop.models import Product, Shop
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon


class OrderInformation(models.Model):
    braintree_id = models.CharField(max_length=150,
                                    blank=True)
    name = models.CharField(max_length=50,
                            blank=False,
                            null=False)
    surname = models.CharField(max_length=50,
                               blank=False,
                               null=False)
    email = models.EmailField(null=False,
                              blank=False)
    address = models.CharField(max_length=100,
                               blank=False,
                               null=False)
    city = models.CharField(max_length=50,
                            blank=False,
                            null=False)
    zipcode = models.CharField(max_length=10,
                               blank=False,
                               null=False)
    coupon = models.ForeignKey(Coupon,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.name} {self.surname}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False,
                                   null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order_information = models.ForeignKey(OrderInformation,
                                          on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.product.name}"

    @property
    def get_total_cost(self):
        return self.product.price * self.quantity

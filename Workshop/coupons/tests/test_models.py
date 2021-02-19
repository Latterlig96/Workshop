from django.test import TestCase
from ..models import Coupon


class CouponTest(TestCase): 

    def test_create_coupon(self):
        coupon = Coupon.objects.create(code="TestCode",
                                       valid_from="2021-07-21",
                                       valid_to="2021-07-30",
                                       discount=10,
                                       active=True)
        self.assertEqual(1, Coupon.objects.count())

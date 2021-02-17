from customer.models import Customer, CustomerProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase


class CustomerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword"
        )

    def test_create_customer(self):
        customer = Customer.objects.create(customer=self.user,
                                           address="ExampleAddress")
        self.assertEqual(1, Customer.objects.count())
        self.assertTrue(customer.customer, self.user)

    def test_create_customer_with_null_address(self):
        with self.assertRaises(IntegrityError):
            customer = Customer.objects.create(customer=self.user,
                                               address=None)
            self.assertEqual(0, Customer.objects.count())


class CustomerProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword"
        )
        self.customer = Customer.objects.create(customer=self.user,
                                                address="ExampleAddress")
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

    def test_create_customer_profile(self):
        customer_profile = CustomerProfile.objects.create(customer=self.customer,
                                                          phone_number="333-333-333",
                                                          image=self.uploaded)
        self.assertEqual(1, CustomerProfile.objects.count())
        self.assertTrue(customer_profile.customer, self.customer)

    def test_invalid_create_customer_profile(self):
        test_cases = [{
            "customer": None,
            "phone_number": "333-333-333",
            "image": self.uploaded,
        },
            {
            "customer": self.customer,
            "phone_number": None,
            "image": self.uploaded,
        }]

        for test_case in test_cases:
            with transaction.atomic():
                customer_profile = CustomerProfile.objects.create(**test_case)
                self.assertTrue(0, CustomerProfile.objects.count())

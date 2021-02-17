from customer.models import Customer
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase
from ..forms import OrderInformationForm


class OrderInformationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword"
        )
        self.customer = Customer.objects.create(
            customer=self.user,
            address="TestAddress"
        )

    def test_create_order_information(self):
        data = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        }
        form = OrderInformationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_order_information_form_creation(self):
        test_cases = [{
            "name": None,
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": None,
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": None,
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": None,
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": None,
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": None
        }]

        for test_case in test_cases:
            with transaction.atomic():
                form = OrderInformationForm(data=test_case)
                self.assertFalse(form.is_valid())

    def test_invalid_email_form(self):
        data = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "UserDoestNotExist@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        }
        form = OrderInformationForm(data=data)
        self.assertFalse(form.is_valid())

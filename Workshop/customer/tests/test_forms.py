from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TestCase
from ..forms import CustomerEditForm, CustomerLoginForm, CustomerRegisterForm
from ..models import Customer


class CustomerRegisterTest(TestCase):

    def test_register_customer_form(self):
        data = {
            "address": "SimpleAddress",
            "email": "SimpleEmail@example.com",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName"
        }

        form = CustomerRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_customer_form_creation(self):
        test_cases = [{
            "address": None,
            "email": "TestEmail@example.com",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName"
        },
            {
            "address": "SimpleAddress",
                       "email": None,
                       "password": "password",
                       "confirm_password": "password",
                       "first_name": "ExampleUser",
                       "last_name": "ExampleUserLastName"
        },
            {
            "address": "",
                       "email": "TestEmail@example.com",
                       "password": "password",
                       "confirm_password": "password",
                       "first_name": "ExampleUser",
                       "last_name": "ExampleUserLastName"
        },
            {
            "address": "SimpleAddress",
                       "email": "",
                       "password": "password",
                       "confirm_password": "password",
                       "first_name": "ExampleUser",
                       "last_name": "ExampleUserLastName"
        }]

        for test_case in test_cases:
            with transaction.atomic():
                form = CustomerRegisterForm(data=test_case)
                self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        data = {
            "address": "SimpleAddress",
            "email": "SimpleEmail@example.com",
            "password": "password",
            "confirm_password": "Not the same",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName"
        }

        form = CustomerRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = {
            "address": "SimpleAddress",
            "email": "This is invalid email",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName"
        }

        form = CustomerRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class CustomerLoginTest(TestCase):

    def test_valid_customer_login(self):
        data = {
            "email": "SimpleEmail@example.com",
            "password": "password"
        }
        form = CustomerLoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        data = {
            "email": "This is not an email",
            "password": "password"
        }
        form = CustomerLoginForm(data=data)
        self.assertFalse(form.is_valid())


class CustomerEditTest(TestCase):

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

    def test_valid_customer_edit(self):
        data = {
            "customer": self.customer,
            "phone_number": "333-333-333",
            "image": self.uploaded
        }
        form = CustomerEditForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_customer_edit_email(self):
        data = {
            "customer": None,
            "phone_number": "333-333-333",
            "image": self.uploaded,
        }
        form = CustomerEditForm(data=data)
        self.assertFalse(form.is_valid())

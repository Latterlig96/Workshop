from http import HTTPStatus
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from ..models import Customer


class CustomerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")

        self.customer = Customer.objects.create(customer=self.user,
                                                address="ExampleAddress")

    def test_get_register_url_by_location(self):
        response = self.client.get('/customer/register/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/register.html')

    def test_get_register_url_by_name(self):
        response = self.client.get(reverse('customer_register'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/register.html')

    def test_get_login_url_by_location(self):
        response = self.client.get('/customer/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/login.html')

    def test_get_login_url_by_name(self):
        response = self.client.get(reverse('customer_login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/login.html')

    def test_get_index_url_by_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_get_index_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_get_settings_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/customer/settings/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/settings.html')

    def test_get_settings_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('customer_settings'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/settings.html')

    def test_get_edit_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/customer/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/edit_profile.html')

    def test_get_edit_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('customer_edit'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/edit_profile.html')

    def test_invalid_user_login(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('customer_login'))
        self.assertNotEqual(response.context['user'], self.customer.customer)

    def test_valid_user_login(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('customer_login'))
        self.assertEqual(response.context['user'], self.customer.customer)

    def test_valid_user_login_dashboard_access(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_invalid_user_login_dashboard_access(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'shop/dashboard.html')

    def test_valid_user_login_settings_access(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('customer_settings'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/settings.html')

    def test_invalid_user_login_settings_access(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('customer_settings'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'customer/settings.html')

    def test_valid_user_login_edit_access(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('customer_edit'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'customer/edit_profile.html')

    def test_invalid_user_login_edit_access(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('customer_edit'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'customer/edit_profile.html')

    def test_valid_user_logout(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'shop/dashboard.html')
        self.assertIsNone(response.context)

    def test_invalid_form_user_login(self):
        response = self.client.post(reverse('customer_login'),
                                    data={'email': "User", "password": "ExamplePassword"})
        self.assertFormError(response, 'form', 'email',
                             "Enter a valid email address.")

    def test_invalid_form_user_password(self):
        response = self.client.post(reverse('customer_login'),
                                    data={'email': "User", "password": ""})
        self.assertFormError(response, 'form', 'password',
                             "This field is required.")

    def test_register_valid_user_post(self):
        data = {
            "address": "SimpleAddress",
            "email": "SimpleEmail@example.com",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName"
        }
        response = self.client.post(reverse('customer_register'), data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_invalid_user_post(self):
        test_cases = [{
            "address": "",
            "email": "SimpleEmail@example.com",
            "password": "password",
                        "confirm_password": "password",
                        "first_name": "ExampleUser",
                        "last_name": "ExampleUserLastName",
                        "error": "This field is required.",
                        "field": "address"
        },
            {
            "address": "SimpleAddress",
            "email": "",
            "password": "password",
                        "confirm_password": "password",
                        "first_name": "ExampleUser",
                        "last_name": "ExampleUserLastName",
                        "error": "This field is required.",
                        "field": "email"
        },
            {
            "address": "SimpleAddress",
            "email": "SimpleEmail",
            "password": "password",
                        "confirm_password": "password",
                        "first_name": "ExampleUser",
                        "last_name": "ExampleUserLastName",
                        "error": "Enter a valid email address.",
                        "field": "email"
        }]

        for test_case in test_cases:
            with transaction.atomic():
                error = test_case.pop("error")
                field = test_case.pop("field")
                response = self.client.post(
                    reverse("customer_register"), data=test_case)
                self.assertFormError(response, 'form', field, error)

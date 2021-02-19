from http import HTTPStatus
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from ..models import Assortment, Category, Employee, Magazine, Owner, Producent, Product, Shop


class EmployeeTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')
        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")

        self.producent = Producent.objects.create(logo=self.uploaded,
                                                  name="TestProducent")
        self.category = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")
        self.product = Product.objects.create(logo=self.uploaded,
                                              name="Product",
                                              description="Example",
                                              category=self.category,
                                              price=20)
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=20,
                                                    category=self.category)
        self.magazine = Magazine.objects.create(address="SimpleMagazine")
        self.magazine.assortment.add(self.assortment)
        self.shop = Shop.objects.create(name="TestShop",
                                        address="TestAdress")
        self.shop.producent.add(self.producent)
        self.shop.magazine.add(self.magazine)
        self.employee = Employee.objects.create(employee=self.user,
                                                shop=self.shop)

    def test_get_register_url_by_location(self):
        response = self.client.get('/shop/register/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/register.html')

    def test_get_register_url_by_name(self):
        response = self.client.get(reverse('employee_register'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/register.html')

    def test_get_login_url_by_location(self):
        response = self.client.get('/shop/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/login.html')

    def test_get_login_url_by_name(self):
        response = self.client.get(reverse('employee_login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/login.html')

    def test_get_index_url_by_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_get_index_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_invalid_user_login(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('employee_login'))
        self.assertNotEqual(response.context['user'], self.employee.employee)

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

    def test_get_settings_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/shop/employee/settings/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, 'shop/employee/employee_settings.html')

    def test_get_settings_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('employee_settings'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, 'shop/employee/employee_settings.html')

    def test_get_edit_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/shop/employee/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/edit_profile.html')

    def test_get_product_detail_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(
            f'/shop/products/detail/{self.product.name}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_get_product_detail_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(
            reverse('product_detail', kwargs={'name': self.product.name}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_get_product_filter_list_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(f'/shop/products/{self.product.name}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/products_list.html')

    def test_get_product_filter_list_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(
            reverse("products_list", kwargs={"filter": self.product.name}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/products_list.html')

    def test_get_product_category_filter_list_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(f'/shop/products/{self.category.name}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/products_list.html')

    def test_get_product_category_filter_list_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("category_products_list", kwargs={
                                   'category': self.category.name}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/products_list.html')

    def test_valid_user_login_settings_access(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('employee_settings'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, 'shop/employee/employee_settings.html')

    def test_invalid_user_login_settings_access(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('employee_settings'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(
            response, 'shop/employee/employee_settings.html')

    def test_valid_user_login_edit_access(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('employee_edit'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/employee/edit_profile.html')

    def test_invalid_user_login_edit_access(self):
        login = self.client.login(
            username="ExampleUser", password="not valid password")
        response = self.client.get(reverse('employee_edit'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'shop/employee/edit_profile.html')

    def test_valid_user_login(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('employee_login'))
        self.assertEqual(response.context['user'], self.employee.employee)

    def test_valid_user_logout(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'shop/dashboard.html')
        self.assertIsNone(response.context)

    def test_invalid_form_user_login(self):
        response = self.client.post(reverse('employee_login'),
                                    data={'email': "User", "password": "ExamplePassword"})
        self.assertFormError(response, 'form', 'email',
                             "Enter a valid email address.")

    def test_invalid_form_user_password(self):
        response = self.client.post(reverse('employee_login'),
                                    data={'email': "User", "password": ""})
        self.assertFormError(response, 'form', 'password',
                             "This field is required.")

    def test_register_valid_user_post(self):
        data = {"address": "SimpleAddress",
                "email": "SimpleEmail@example.com",
                "password": "password",
                "confirm_password": "password",
                "first_name": "ExampleUser",
                "last_name": "ExampleUserLastName",
                "shop": self.shop}
        response = self.client.post(reverse('employee_register'), data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_invalid_user_post(self):
        test_cases = [{"email": "",
                       "password": "password",
                       "confirm_password": "password",
                       "first_name": "ExampleUser",
                       "last_name": "ExampleUserLastName",
                       "shop": self.shop,
                       "error": "This field is required.",
                       "field": "email"
                       },
                      {"email": "SimpleEmail@example.com",
                       "password": "password",
                       "confirm_password": "password",
                       "first_name": "ExampleUser",
                       "last_name": "ExampleUserLastName",
                       "shop": "",
                       "error": "This field is required.",
                       "field": "shop"
                       },
                      {"email": "SimpleEmail",
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
                    reverse("employee_register"), data=test_case)
                self.assertFormError(response, 'form', field, error)

    def test_create_order_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        }
        response = self.client.post(reverse('product_order', kwargs={'product': self.product.name}),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'order/order_done.html')

    def test_invalid_create_order_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_cases = [{
            "name": '',
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": '',
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": '',
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": '',
            "city": "TestCity",
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": '',
            "zipcode": "TestZipCode"
        },
            {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "User@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": ''
        }]

        for test_case in test_cases:
            with transaction.atomic():
                response = self.client.post(reverse('product_order', kwargs={'product': self.product.name}),
                                            data=test_case)
                self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertTemplateNotUsed(response, 'order/order_done.html')

    def test_invalid_email_order_create_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "UserDoesNotExist@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "TestZipCode"
        }
        response = self.client.post(reverse('product_order', kwargs={'product': self.product.name}),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertFormError(response, 'form', 'email',
                             f"Email {data['email']} doest not exist")


class OwnerTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")

        self.producent = Producent.objects.create(logo=self.uploaded,
                                                  name="TestProducent")
        self.category = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")
        self.product = Product.objects.create(logo=self.uploaded,
                                              name="Product",
                                              description="Example",
                                              category=self.category,
                                              price=20)
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=20,
                                                    category=self.category)
        self.magazine = Magazine.objects.create(address="SimpleMagazine")
        self.magazine.assortment.add(self.assortment)
        self.shop = Shop.objects.create(name="TestShop",
                                        address="TestAdress")
        self.shop.producent.add(self.producent)
        self.shop.magazine.add(self.magazine)
        self.owner = Owner.objects.create(owner=self.user,
                                          shop=self.shop,
                                          has_ownership=True)

    def test_get_owner_settings_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/shop/owner/settings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/owner/owner_settings.html')

    def test_get_owner_settings_url_by_name(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('owner_settings'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/owner/owner_settings.html')

    def test_get_owner_dashboard_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get('/shop/owner/panel/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/owner/owner_dashboard.html')

    def test_get_owner_dashboard_url_by_location(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('owner_dashboard'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/owner/owner_dashboard.html')

    def test_create_producent_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "name": "TestName",
            "logo": self.uploaded,
        }
        response = self.client.post(reverse('new_producent_register'),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_create_product_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "name": "TestName",
            "logo": self.uploaded,
            "price": 100,
            "category": self.category,
        }
        response = self.client.post(reverse('new_product_register'),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_create_category_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "name": "TestName",
            "category_logo": self.uploaded,
        }
        response = self.client.post(reverse('new_category_register'),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_create_assortment_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "product": self.product,
            "quantity": 20,
            "category": self.category,
        }
        response = self.client.post(reverse('new_assortment_register'),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_create_magazine_view(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        data = {
            "address": "TestAddress",
            "assortment": self.assortment,
        }
        response = self.client.post(reverse('new_magazine_register'),
                                    data=data)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/dashboard.html')

    def test_invalid_producent_create(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_case = {
            "name": '',
            "logo": self.uploaded
        }
        response = self.client.post(
            reverse('new_producent_register'), data=test_case)
        self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'shop/dashboard.html')

    def test_invalid_product_create(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_cases = [{
            "name": '',
            "logo": self.uploaded,
            "price": 100,
            "category": self.category,
        },
            {
            "name": "TestName",
            "logo": self.uploaded,
            "price": '',
            "category": self.category,
        },
            {
            "name": "TestName",
            "logo": self.uploaded,
            "price": 100,
            "category": '',
        }]
        for test_case in test_cases:
            with transaction.atomic():
                response = self.client.post(reverse('new_product_register'),
                                            data=test_case)
                self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertTemplateNotUsed(response, 'order/dashboard.html')

    def test_invalid_category_create(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_case = {
            "name": '',
            "category_logo": self.uploaded,
        }
        response = self.client.post(
            reverse('new_category_register'), data=test_case)
        self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, 'shop/dashboard.html')

    def test_invalid_assortment_create(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_cases = [{
            "product": '',
            "quantity": 20,
            "category": self.category,
        },
            {
            "product": self.product,
            "quantity": '',
            "category": self.category,
        },
            {
            "product": self.product,
            "quantity": 20,
            "category": '',
        }]

        for test_case in test_cases:
            with transaction.atomic():
                response = self.client.post(reverse('new_assortment_register'),
                                            data=test_case)
                self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertTemplateNotUsed(response, 'order/dashboard.html')

    def test_invalid_magazine_create(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        test_cases = [
            {
                "address": '',
                "assortment": self.assortment,
            },
            {
                "address": "TestAddress",
                "assortment": '',
            }
        ]
        for test_case in test_cases:
            with transaction.atomic():
                response = self.client.post(reverse('new_magazine_register'),
                                            data=test_case)
                self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertTemplateNotUsed(response, 'order/dashboard.html')

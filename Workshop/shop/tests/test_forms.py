from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TestCase
from ..forms import AssortmentRegisterForm, CategoryRegisterForm, EmployeeEditForm, EmployeeLoginForm, \
    EmployeeRegisterForm, MagazineRegisterForm, ProducentRegisterForm, ProductRegisterForm
from ..models import Assortment, Category, Employee, Magazine, Producent, Product, Shop


class EmployeeRegisterTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

        self.producent = Producent.objects.create(name="TestProducent")
        self.category = Category.objects.create(name="TestCategory")
        self.product = Product.objects.create(name="Product",
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

    def test_register_employee_form(self):
        data = {
            "address": "SimpleAddress",
            "email": "SimpleEmail@example.com",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": self.shop
        }

        form = EmployeeRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_employee_form_creation(self):
        test_cases = [{
            "email": None,
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": self.shop
        },
            {
            "email": "TestEmail@example.com",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": None
        },
            {
            "email": "",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": self.shop
        }]

        for test_case in test_cases:
            with transaction.atomic():
                form = EmployeeRegisterForm(data=test_case)
                self.assertFalse(form.is_valid())

    def test_invalid_password(self):
        data = {
            "address": "SimpleAddress",
            "email": "SimpleEmail@example.com",
            "password": "password",
            "confirm_password": "Not the same",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": self.shop
        }

        form = EmployeeRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = {
            "address": "SimpleAddress",
            "email": "This is invalid email",
            "password": "password",
            "confirm_password": "password",
            "first_name": "ExampleUser",
            "last_name": "ExampleUserLastName",
            "shop": self.shop
        }

        form = EmployeeRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class EmployeeLoginTest(TestCase):

    def test_valid_employee_login(self):
        data = {
            "email": "SimpleEmail@example.com",
            "password": "password"
        }
        form = EmployeeLoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        data = {
            "email": "This is not an email",
            "password": "password"
        }
        form = EmployeeLoginForm(data=data)
        self.assertFalse(form.is_valid())


class EmployeeProfileTest(TestCase):

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

        self.producent = Producent.objects.create(name="TestProducent")
        self.category = Category.objects.create(name="TestCategory")
        self.product = Product.objects.create(name="Product",
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

    def test_valid_employee_profile(self):
        data = {
            "employee": self.employee,
            "phone_numer": "333-333-333",
            "image": self.uploaded,
        }
        form = EmployeeEditForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_customer_profile_create(self):
        data = {
            "employee": None,
            "phone-number": "333-333-333",
            "image": self.uploaded
        }
        form = EmployeeEditForm(data=data)
        self.assertFalse(form.is_valid())


class ProducentRegisterTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

    def test_valid_producent_register(self):
        data = {
            'logo': self.uploaded,
            'name': "TestProducent"
        }
        form = ProducentRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_producent_name(self):
        data = {
            'logo': self.uploaded,
            'name': ''
        }
        form = ProducentRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class CategoryRegisterForm(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

    def test_category_register_form(self):
        data = {
            'category_logo': self.uploaded,
            'name': "TestName"
        }
        form = CategoryRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_category_register(self):
        data = {
            'category_logo': self.uploaded,
            'name': ''
        }
        form = CategoryRegisterForm(data=data)
        self.assertFalse(form.is_valid())


class ProductRegisterTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')
        self.category = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")

    def test_product_register_form(self):
        data = {
            "logo": self.uploaded,
            "name": "TestProduct",
            "price": 20,
            "category": self.category,
            "description": "TestDescription"
        }
        form = ProductRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_product_register(self):
        test_cases = [
            {
                "logo": self.uploaded,
                "name": '',
                "price": 20,
                "category": self.category,
                "description": "TestDescription"
            },
            {
                "logo": self.uploaded,
                "name": "TestProduct",
                "price": '',
                "category": self.category,
                "description": "TestDescription"
            },
            {
                "logo": self.uploaded,
                "name": "TestProduct",
                "price": "TestPrice",
                "category": '',
                "description": "TestDescription"
            },
        ]

        for test_case in test_cases:
            with transaction.atomic():
                form = ProductRegisterForm(data=test_case)
                self.assertFalse(form.is_valid())


class AssortmentRegisterTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

        self.category = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")
        self.product = Product.objects.create(logo=self.uploaded,
                                              name="TestName",
                                              price=20,
                                              category=self.category,
                                              description="TestDescription")

    def test_assortment_register_form(self):
        data = {
            'product': self.product,
            'quantity': 20,
            'category': self.category
        }
        form = AssortmentRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_assortment_form(self):
        test_cases = [{
            'product': '',
            'quantity': 20,
            'category': self.category
        },
            {
            'product': self.product,
            'quantity': '',
            'category': self.category
        },
            {
            'product': self.product,
            'quantity': 20,
            'category': ''
        },
        ]

        for test_case in test_cases:
            with transaction.atomic():
                form = AssortmentRegisterForm(data=test_case)
                self.assertFalse(form.is_valid())


class MagazineRegisterTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')
        self.category = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")
        self.product = Product.objects.create(logo=self.uploaded,
                                              name="TestName",
                                              price=20,
                                              category=self.category,
                                              description="TestDescription")
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=20,
                                                    category=self.category)

    def test_magazine_register_form(self):
        data = {
            'address': "TestAddress",
            "assortment": self.assortment
        }
        form = MagazineRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_magazine_register(self):
        test_cases = [
            {
                'address': '',
                'assortment': self.assortment
            },
            {
                'address': "TestAddress",
                'assortment': ''
            }
        ]

        for test_case in test_cases:
            with transaction.atomic():
                form = MagazineRegisterForm(data=test_case)
                self.assertFalse(form.is_valid())

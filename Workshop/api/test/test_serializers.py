from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TestCase
from customer.models import Customer
from shop.models import Assortment, Category, Employee, Magazine, Producent, Product, Shop
from ..serializers import EmployeeSerializer, OrderInformationSerializer, ProductSerializer, RegisterCustomerSerializer


class RegisterCustomerSerializerTest(TestCase):

    def setUp(self):
        self.data = {
            "first_name": "TestName",
            "last_name": "TestLastName",
            "email": "exampleemail@example.com",
            "address": "TestAddress",
            "password": "TestPassword",
            "password2": "TestPassword"
        }

    def test_form_valid(self):
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_customer_create(self):
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.create(self.data)
        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, Customer.objects.count())

    def test_invalid_password(self):
        self.data['password'] = "Invalid"
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['password']))

    def test_empty_required_arguments(self):
        test_cases = [
            {
                "first_name": None,
                "last_name": "TestLastName",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "password": "TestPassword",
                "password2": "TestPassword",
                "error_field": "first_name"
            },
            {
                "first_name": "TestFirstName",
                "last_name": None,
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "password": "TestPassword",
                "password2": "TestPassword",
                "error_field": "last_name"
            },
            {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "email": None,
                "address": "TestAddress",
                "password": "TestPassword",
                "password2": "TestPassword",
                "error_field": "email"
            },
            {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "email": "exampleemail@example.com",
                "address": None,
                "password": "TestPassword",
                "password2": "TestPassword",
                "error_field": "address"
            },
            {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "password": None,
                "password2": "TestPassword",
                "error_field": "password"
            },
            {
                "first_name": "TestFirstName",
                "last_name": "TestLastName",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "password": "TestPassword",
                "password2": None,
                "error_field": "password2"
            }
        ]
        for test_case in test_cases:
            with transaction.atomic():
                error_field = test_case.pop('error_field')
                serializer = RegisterCustomerSerializer(data=test_case)
                self.assertFalse(serializer.is_valid())
                self.assertEqual(set(serializer.errors.keys()),
                                 set([error_field]))


class EmployeeSerializerTest(TestCase):

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
        self.data = {"employee": self.employee,
                     "shop": self.shop}

    def test_form_valid(self):
        serializer = EmployeeSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())


class ProductSerializerTest(TestCase):

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

        self.data = {
            'name': "TestProduct",
            'price': 30,
            'category': self.category,
            'description': "TestDescription"
        }

    def test_form_valid(self):
        serializer = ProductSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_empty_fields(self):
        test_cases = [
            {
                "name": None,
                "price": 30,
                "category": self.category,
                "description": "TestDescription",
                "error_field": "name"
            },
            {
                "name": "TestProduct",
                "price": None,
                "category": self.category,
                "description": "TestDescription",
                "error_field": "price"
            },
            {
                "name": "TestProduct",
                "price": 30,
                "category": None,
                "description": "TestDescription",
                "error_field": "category"
            }
        ]

        for test_case in test_cases:
            with transaction.atomic():
                error_field = test_case.pop('error_field')
                serializer = ProductSerializer(data=test_case)
                self.assertFalse(serializer.is_valid())
                self.assertEqual(set(serializer.errors.keys()),
                                 set([error_field]))


class OrderInformationSerializerTest(TestCase):

    def setUp(self):
        self.data = {
            "name": "TestName",
            "surname": "TestSurname",
            "email": "exampleemail@example.com",
            "address": "TestAddress",
            "city": "TestCity",
            "zipcode": "33-333"
        }

    def test_form_valid(self):
        serializer = OrderInformationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_empty_fields(self):
        test_cases = [
            {
                "name": None,
                "surname": "TestSurname",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "city": "TestCity",
                "zipcode": "33-333",
                "error_field": "name"
            },
            {
                "name": "TestName",
                "surname": None,
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "city": "TestCity",
                "zipcode": "33-333",
                "error_field": "surname"
            },
            {
                "name": "TestName",
                "surname": "TestSurname",
                "email": None,
                "address": "TestAddress",
                "city": "TestCity",
                "zipcode": "33-333",
                "error_field": "email"
            },
            {
                "name": "TestName",
                "surname": "TestSurname",
                "email": "exampleemail@example.com",
                "address": None,
                "city": "TestCity",
                "zipcode": "33-333",
                "error_field": "address"
            },
            {
                "name": "TestName",
                "surname": "TestSurname",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "city": None,
                "zipcode": "33-333",
                "error_field": "city"
            },
            {
                "name": "TestName",
                "surname": "TestSurname",
                "email": "exampleemail@example.com",
                "address": "TestAddress",
                "city": "TestCity",
                "zipcode": None,
                "error_field": "zipcode"
            }
        ]

        for test_case in test_cases:
            with transaction.atomic():
                error_field = test_case.pop('error_field')
                serializer = OrderInformationSerializer(data=test_case)
                self.assertFalse(serializer.is_valid())
                self.assertEqual(set(serializer.errors.keys()),
                                 set([error_field]))

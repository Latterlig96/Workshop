from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from shop.models import Assortment, Category, Magazine, Producent, Product, Shop
from ..models import OrderInformation, OrderItem


class OrderInformationTest(TestCase):

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
        self.product = Product.objects.create(name="Product",
                                              description="Example",
                                              category=self.category,
                                              price=20)
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=50,
                                                    category=self.category)
        self.magazine = Magazine.objects.create(address="ExampleAddress")
        self.magazine.assortment.add(self.assortment)
        self.producent = Producent.objects.create(logo=self.uploaded,
                                                  name="TestProducent")
        self.shop = Shop.objects.create(name="TestShop",
                                        address="Address")
        self.shop.producent.add(self.producent)
        self.shop.magazine.add(self.magazine)

    def test_create_order_information(self):
        order_information = OrderInformation.objects.create(name="OrderName",
                                                            surname="OrderSurname",
                                                            email="Order@example.com",
                                                            address="ServiceAddress",
                                                            city="TestCity",
                                                            zipcode="300-300")
        self.assertEqual(1, OrderInformation.objects.count())

    def test_create_order_information_with_null_values(self):
        test_cases = [{
            "name": None,
            "surname": "Simple Surname",
            "email": "simple@example.com",
            "address": "simpleaddress",
            "city": "TestCity",
            "zipcode": "300-300",
        },
            {
            "name": "SimpleName",
            "surname": None,
            "email": "simple@example.com",
            "address": "simpleaddress",
            "city": "TestCity",
            "zipcode": "300-300",
        },
            {
            "name": "SimpleName",
            "surname": "Simple Surname",
            "email": None,
            "address": "simpleaddress",
            "city": "TestCity",
            "zipcode": "300-300",
        },
            {
            "name": "SimpleName",
            "surname": "Simple Surname",
            "email": "simple@example.com",
            "address": None,
            "city": "TestCity",
            "zipcode": "300-300",
        },
            {
            "name": "SimpleName",
            "surname": "Simple Surname",
            "email": "simple@example.com",
            "address": "simpleaddress",
            "city": None,
            "zipcode": "300",
        },
            {
            "name": "SimpleName",
            "surname": "Simple Surname",
            "email": "simple@example.com",
            "address": "simpleaddress",
            "city": "TestCity",
            "zipcode": None,
        }
        ]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    order_information = OrderInformation.objects.create(
                        **test_case)
                    self.assertEqual(0, OrderInformation.objects.count())


class OrderItemTest(TestCase):

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
        self.product = Product.objects.create(name="Product",
                                              description="Example",
                                              category=self.category,
                                              price=20)
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=50,
                                                    category=self.category)
        self.magazine = Magazine.objects.create(address="ExampleAddress")
        self.magazine.assortment.add(self.assortment)
        self.producent = Producent.objects.create(logo=self.uploaded,
                                                  name="TestProducent")
        self.shop = Shop.objects.create(name="TestShop",
                                        address="Address",)
        self.shop.producent.add(self.producent)
        self.shop.magazine.add(self.magazine)
        self.order_information = OrderInformation.objects.create(name="OrderName",
                                                                 surname="OrderSurname",
                                                                 email="Order@example.com",
                                                                 address="ServiceAddress",
                                                                 city="TestCity",
                                                                 zipcode="300-300")

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(product=self.product,
                                              quantity=20,
                                              order_information=self.order_information,
                                              shop=self.shop)
        self.assertEqual(1, OrderItem.objects.count())

    def test_create_order_item_with_null_values(self):
        test_cases = [{
            "product": None,
            "quantity": 20,
            "order_information": self.order_information,
            "shop": self.shop,
        },
            {
            "product": self.product,
            "quantity": None,
            "order_information": self.order_information,
            "shop": self.shop,
        },
            {
            "product": self.product,
            "quantity": 20,
            "order_information": None,
            "shop": self.shop,
        },
            {
            "product": self.product,
            "quantity": 20,
            "order_information": self.order_information,
            "shop": None,
        }]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    order_item = OrderItem.objects.create(**test_case)
                    self.assertEqual(0, OrderItem.objects.count())

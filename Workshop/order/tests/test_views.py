from http import HTTPStatus
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase
from shop.models import Assortment, Category, Employee, Magazine, Producent, Product, Shop
from ..models import OrderInformation, OrderItem


class OrderTest(TestCase):

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
            password="ExamplePassword"
        )

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

        self.order_information = OrderInformation.objects.create(name="TestName",
                                                                 surname="TestSurname",
                                                                 email="TestEmail@example.com",
                                                                 address="TestAddress",
                                                                 city="TestCity",
                                                                 zipcode="33-333")
        self.order_item = OrderItem.objects.create(product=self.product,
                                                   quantity=20,
                                                   order_information=self.order_information,
                                                   shop=self.shop)

    def test_payment_link_send(self):
        login = self.client.login(
            username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse('payment_link_send', kwargs={
                                   'id': self.order_item.order_information.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'order/order_link_sent_success.html')

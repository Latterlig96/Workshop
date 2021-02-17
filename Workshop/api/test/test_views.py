from http import HTTPStatus
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from customer.models import Customer
from order.models import OrderInformation, OrderItem
from shop.models import Assortment, Category, Employee, Magazine, Producent, Product, Shop
from ..serializers import EmployeeSerializer, ProductSerializer


class ProductTest(TestCase):

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
                                              name="Product",
                                              description="Example",
                                              category=self.category,
                                              price=20)

    def test_product_list(self):
        response = self.client.get('/api/product/list', format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        product = ProductSerializer(self.product)
        self.assertTrue(response.json(), product.data)

    def test_product_detail(self):
        response = self.client.get(
            f'/api/product/{self.product.id}', format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        product = ProductSerializer(self.product)
        self.assertTrue(response.json(), product.data)

    def test_invalid_product_detail(self):
        response = self.client.get(f'/api/product/{20}', format='json')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class RegisterCustomerTest(TestCase):

    def setUp(self):
        self.data = {
            'first_name': "TestCustomer",
            'last_name': "TestLastNameCustomer",
            'email': "ExampleCustomer@example.com",
            'password': "TestPassword",
            'password2': "TestPassword"
        }

    def register_valid_customer(self):
        response = self.client.post('/api/customer/register', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, Customer.objects.count())

    def test_invalid_password(self):
        self.data['password'] = "Nothing"
        response = self.client.post('/api/customer/register', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)
        self.assertNotEqual(1, User.objects.count())
        self.assertNotEqual(1, Customer.objects.count())

    def test_invalid_email(self):
        self.data['email'] = "ExampleInvalidEmail"
        response = self.client.post('/api/customer/register', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)
        self.assertNotEqual(1, User.objects.count())
        self.assertNotEqual(1, Customer.objects.count())

    def test_invalid_first_name(self):
        self.data['first_name'] = ""
        response = self.client.post('/api/customer/register', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)
        self.assertNotEqual(1, User.objects.count())
        self.assertNotEqual(1, Customer.objects.count())

    def test_invalid_last_name(self):
        self.data['last_name'] = ""
        response = self.client.post('/api/customer/register', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)
        self.assertNotEqual(1, User.objects.count())
        self.assertNotEqual(1, Customer.objects.count())


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

    def test_employee_list(self):
        response = self.client.get('/api/employee/list', format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        employee = EmployeeSerializer(self.employee)
        self.assertTrue(response.json(), employee.data)

    def test_employee_detail(self):
        response = self.client.get(
            f'/api/employee/{self.employee.id}', format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        employee = EmployeeSerializer(self.employee)
        self.assertTrue(response.json(), employee.data)

    def test_invalid_employee_detail(self):
        response = self.client.get(f'/api/employee/{20}', format='json')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class OrderInformationTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

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
        self.data = {"name": "TestName",
                     "surname": "TestSurname",
                     "email": "TestEmail@example.com",
                     "address": "TestAddress",
                     "city": "TestCity",
                     "zipcode": "33-333"}

    def register_valid_order(self):
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(1, OrderInformation.objects.count())
        self.assertEqual(1, OrderItem.objects.count())

    def test_invalid_email(self):
        self.data['email'] = "OrderInvalidEmail"
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

    def test_invalid_name(self):
        self.data['name'] = ""
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

    def test_invalid_surname(self):
        self.data['surname'] = ""
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

    def test_invalid_address(self):
        self.data['address'] = ""
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

    def test_invalid_city(self):
        self.data['city'] = ""
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

    def test_invalid_zipcode(self):
        self.data['zipcode'] = ""
        response = self.client.post(
            f'/api/order/create/{self.product.name}', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotEqual(1, OrderInformation.objects.count())
        self.assertNotEqual(1, OrderItem.objects.count())

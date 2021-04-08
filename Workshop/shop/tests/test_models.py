from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
import datetime
from django.db.utils import IntegrityError
from django.test import TestCase
from shop.models import Assortment, Category, Employee, EmployeeProfile, Magazine, Producent, Product, Shop, Owner, OwnerProfile, Task


class ProducentTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

    def test_producent_create(self):
        producent = Producent.objects.create(logo=self.uploaded,
                                             name="TestProducent")
        self.assertEqual(1, Producent.objects.count())

    def test_producent_with_same_name(self):
        producent = Producent.objects.create(logo=self.uploaded,
                                             name="TestProducent")
        self.assertEqual(1, Producent.objects.count())
        with self.assertRaises(IntegrityError):
            producent2 = Producent.objects.create(logo=self.uploaded,
                                                  name="TestProducent")
            self.assertEqual(1, Producent.objects.count())

    def test_create_producent_with_null_name(self):
        producent = Producent.objects.create(logo=self.uploaded, name=None)
        with self.assertRaises(IntegrityError):
            producent = Producent.objects.create(logo=self.uploaded, name=None)
            self.assertEqual(1, Producent.objects.count())

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

    def test_product_create(self):
        product = Product.objects.create(logo=self.uploaded,
                                         name="TestProduct",
                                         description="Simple",
                                         category=self.category,
                                         price=20)
        self.assertEqual(1, Product.objects.count())

    def test_product_with_same_name(self):
        product = Product.objects.create(logo=self.uploaded,
                                         name="TestProduct",
                                         description="Simple",
                                         category=self.category,
                                         price=20)
        self.assertEqual(1, Product.objects.count())
        with self.assertRaises(IntegrityError):
            product2 = Product.objects.create(logo=self.uploaded,
                                              name="TestProduct",
                                              description="Simple",
                                              category=self.category,
                                              price=20)
            self.assertEqual(1, Product.objects.count())

    def test_create_product_with_null_values(self):
        test_cases = [{
            "name": None,
            "description": "Simple",
            "category": self.category,
            "price": 20,
        },
            {
            "name": "SimpleName",
            "description": None,
            "category": self.category,
            "price": 20,
        },
            {
            "name": "SimpleName",
            "description": "Simple",
            "category": None,
            "price": 20,
        }, {
            "name": "SimpleName",
            "description": "Simple",
            "category": self.category,
            "price": None,
        }]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    product = Product.objects.create(**test_case)
                    self.assertEqual(0, Product.objects.count())


class CategoryTest(TestCase):

    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')

    def test_category_create(self):
        category = Category.objects.create(category_logo=self.uploaded,
                                           name="TestCategory")
        self.assertEqual(1, Category.objects.count())

    def test_category_with_same_name(self):
        category = Category.objects.create(category_logo=self.uploaded,
                                           name="TestCategory")
        self.assertEqual(1, Category.objects.count())
        with self.assertRaises(IntegrityError):
            category2 = Category.objects.create(category_logo=self.uploaded,
                                                name="TestCategory")
            self.assertEqual(1, Category.objects.count())

    def test_create_category_with_null_name(self):
        category = Category.objects.create(category_logo=self.uploaded,
                                           name=None)
        with self.assertRaises(IntegrityError):
            category = Category.objects.create(category_logo=self.uploaded,
                                               name=None)
            self.assertEqual(1, Category.objects.count())


class AssortmentTest(TestCase):

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
                                              name="TestProduct",
                                              description="Simple",
                                              category=self.category,
                                              price=20)

    def test_assortment_create(self):
        assortment = Assortment.objects.create(product=self.product,
                                               quantity=20,
                                               category=self.category)
        self.assertEqual(1, Assortment.objects.count())

    def test_assortment_create_with_null_values(self):
        test_cases = [{
            'product': None,
            'quantity': 30,
            'category': self.category
        },
            {
            'product': self.product,
            'quantity': None,
            'category': self.category
        },
            {
            'product': self.product,
            'quantity': 20,
            'category': None}]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    order = Assortment.objects.create(**test_case)
                    self.assertEqual(0, Assortment.objects.count())


class MagazineTest(TestCase):

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
        self.assortment = Assortment.objects.create(product=self.product,
                                                    quantity=20,
                                                    category=self.category)

    def test_magazine_create(self):
        magazine = Magazine.objects.create(address="TestMagazine")
        magazine.assortment.add(self.assortment)
        self.assertEqual(1, Magazine.objects.count())

    def test_create_magazine_with_null_values(self):
        test_case = {
            "address": None,
        }

        with self.assertRaises(IntegrityError):
            magazine = Magazine.objects.create(**test_case)
            self.assertEqual(0, Magazine.objects.count())

    def test_create_magazine_add_assortment(self):
        magazine = Magazine.objects.create(address="TestAddresss")
        magazine.assortment.add(self.assortment)
        self.assertEqual(1, Magazine.objects.count())
        self.assertTrue(magazine.assortment, self.assortment)


class ShopTest(TestCase):

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

    def test_shop_create(self):
        shop = Shop.objects.create(name="TestShop",
                                   address="SimpleAddress")
        shop.producent.add(self.producent)
        shop.magazine.add(self.magazine)
        self.assertEqual(1, Shop.objects.count())

    def test_shop_create_with_null_values(self):
        test_cases = [{
            "name": None,
            "address": "SimpleAddress",
        },
            {
            "name": "TestName",
            "address": None,
        }
        ]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    shop = Shop.objects.create(**test_case)
                    self.assertEqual(0, Shop.objects.count())

    def test_shop_producent_magazine_add(self):
        data = {
            "name": "SimpleName",
            "address": "SimpleAddress",
        }
        shop = Shop.objects.create(**data)
        shop.producent.add(self.producent)
        shop.magazine.add(self.magazine)
        self.assertEqual(1, Shop.objects.count())
        self.assertTrue(shop.producent, self.producent)
        self.assertTrue(shop.magazine, self.magazine)


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

    def test_create_employee(self):
        employee = Employee.objects.create(employee=self.user,
                                           shop=self.shop)
        self.assertEqual(1, Employee.objects.count())
        self.assertTrue(Employee.employee, self.user)

    def test_create_employee_with_null_values(self):
        test_cases = [{
            "employee": None,
            "shop": self.shop
        },
            {
            "employee": self.user,
            "shop": None}]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    employee = Employee.objects.create(**test_case)
                    self.assertEqual(0, Employee.objects.count())


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

    def test_create_employee_profile(self):
        employee_profile = EmployeeProfile.objects.create(employee=self.employee,
                                                          phone_number="333-333-333",
                                                          image=self.uploaded)
        self.assertEqual(1, EmployeeProfile.objects.count())
        self.assertTrue(employee_profile.employee, self.employee)

    def test_invalid_create_employee_profile(self):
        test_cases = [{
            "employee": None,
            "phone_number": "333-333-333",
            "image": self.uploaded,
        },
            {
            "employee": self.employee,
            "phone_number": None,
            "image": self.uploaded,
        },
            {
            "employee": self.employee,
            "phone_number": "333-333-333",
            "image": None,
        }]

        for test_case in test_cases:
            with transaction.atomic():
                employee_profile = EmployeeProfile.objects.create(**test_case)
                self.assertTrue(0, EmployeeProfile.objects.count())

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

    def test_create_owner(self): 
        owner = Owner.objects.create(owner=self.user,
                                     shop=self.shop,
                                     has_ownership=True)
        self.assertEqual(1, Owner.objects.count())
    
    def test_create_owner_null_values(self): 
        test_cases = [{
            "owner": None,
            "shop": self.shop,
            "has_ownership": True
        },
        {
            "owner": self.user,
            "shop": None,
            "has_ownership": True
        }]

        for test_case in test_cases: 
            with transaction.atomic(): 
                owner = Owner.objects.create(**test_case)
                self.assertEqual(0, Owner.objects.count()) 

class OwnerProfileTest(TestCase):
    
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

    def test_create_owner_profile(self):
        owner_profile = OwnerProfile.objects.create(owner=self.owner,
                                                    phone_number="333-333-333",
                                                    image=self.uploaded)
        self.assertEqual(1, OwnerProfile.objects.count())
        self.assertTrue(owner_profile.owner, self.owner)
    
    def test_invalid_create_owner_profile(self):
        test_cases = [{
            "owner": None,
            "phone_number": "333-333-333",
            "image": self.uploaded,
        },
            {
            "owner": self.owner,
            "phone_number": None,
            "image": self.uploaded,
        },
            {
            "owner": self.owner,
            "phone_number": "333-333-333",
            "image": None,
        }]

        for test_case in test_cases:
            with transaction.atomic():
                owner_profile = OwnerProfile.objects.create(**test_case)
                self.assertTrue(0, OwnerProfile.objects.count())


class TaskTest(TestCase): 

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
        
        self.user_employee = User.objects.create_user(username="ExampleEmployee",
                                                      email="Example@example.com",
                                                      first_name="Employee",
                                                      last_name="Employee",
                                                      password="SimpleEmployee")

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
        self.employee = Employee.objects.create(employee=self.user_employee,
                                             shop=self.shop)
    
    def test_task_create(self): 
        task = Task.objects.create(task_from=self.owner,
                                   task_to=self.employee, 
                                   status='assigned',
                                   description='simple description for task',
                                   execution_time=datetime.date(2020, 10, 15))
        self.assertEqual(1, Task.objects.count()) 
    
    def test_task_create_null_values(self): 
        test_cases = [{
            "task_from": None, 
            "task_to": self.employee, 
            "status": "assigned",
            "description": "simple description for task",
            "execution_time": datetime.date(2020, 10, 150)
        },
        {
            "task_from": self.owner, 
            "task_to": None, 
            "status": "assigned",
            "description": "simple description for task",
            "execution_time": datetime.date(2020, 10, 150)
        },
        {
            "task_from": self.owner, 
            "task_to": self.employee, 
            "status": None,
            "description": "simple description for task",
            "execution_time": datetime.date(2020, 10, 150)
        },
        {
            "task_from": self.owner, 
            "task_to": self.employee, 
            "status": "assigned",
            "description": "simple description for task",
            "execution_time": None
        }]

        for test_case in test_cases: 
            with transaction.atomic(): 
                task = Task.objects.create(**test_case)
                self.assertEqual(0, Task.objects.count()) 

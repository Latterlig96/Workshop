from django.test import TestCase
from ..models import Forum, Thread, Post, Comments
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Producent, Category, Product, Assortment,\
                        Magazine, Shop
from django.contrib.auth.models import Group, User
from django.db.utils import IntegrityError
from django.db import transaction


class ForumTest(TestCase):

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
        self.group = Group.objects.create(name="TestGroup")
    
    def test_create_forum(self): 
        forum = Forum.objects.create(shop=self.shop,
                                     title="TestTitle",
                                     description="TestDescription",
                                     threads=0,
                                     posts=0)
        forum.groups.add(self.group)
        self.assertEqual(1, Forum.objects.count())
    
    def test_create_forum_null_values(self): 
        test_cases = [
        {
            "groups": self.group,
            "shop": None,
            "title": "TestTitle",
            "description": "TestDescription",
            "threads": 0,
            "posts": 0
        },
        {
            "groups": self.group,
            "shop": self.shop,
            "title": None,
            "description": "TestDescription",
            "threads": 0,
            "posts": 0
        },
        {
            "groups": self.group,
            "shop": self.shop,
            "title": "TestTitle",
            "description": None,
            "threads": 0,
            "posts": 0
        }]

        for test_case in test_cases:
            with transaction.atomic():
                group = test_case.pop("groups")
                with self.assertRaises(IntegrityError):
                    forum = Forum.objects.create(**test_case)
                    forum.groups.add(group)
                    self.assertEqual(0, Forum.objects.count())

class ThreadTest(TestCase): 

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
        self.group = Group.objects.create(name="TestGroup")
        self.forum = Forum.objects.create(shop=self.shop,
                                          title="TestTitle",
                                          description="TestDescription",
                                          threads=0,
                                          posts=0)
        self.forum.groups.add(self.group)
    
    def test_create_thread(self): 
        thread = Thread.objects.create(forum=self.forum,
                                       title="TestTitle",
                                       posts=0,
                                       views=0,
                                       closed=False)
        self.assertEqual(1, Thread.objects.count())
    
    def test_create_thread_null_values(self):
        test_cases = [{
            "forum": None,
            "title": "TestTitle",
            "posts": 0,
            "views": 0,
            "closed": False
        },
        {
            "forum": self.forum,
            "title": None,
            "posts": 0,
            "views": 0,
            "closed": False
        }]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    thread = Thread.objects.create(**test_case)
                    self.assertEqual(0, Thread.objects.count())
    

class PostTest(TestCase):

    def setUp(self): 
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")

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
        self.group = Group.objects.create(name="TestGroup")
        self.forum = Forum.objects.create(shop=self.shop,
                                          title="TestTitle",
                                          description="TestDescription",
                                          threads=0,
                                          posts=0)
        self.forum.groups.add(self.group)
        self.thread = Thread.objects.create(forum=self.forum,
                                            title="TestTitle",
                                            posts=0,
                                            views=0,
                                            closed=False)
    
    def test_post_create(self): 
        post = Post.objects.create(thread=self.thread,
                                   author=self.user,
                                   body="TestBody")
        self.assertEqual(1, Post.objects.count())

    def test_post_create_null_values(self): 
        test_cases = [{
            "thread": None,
            "author": self.user,
            "body": "TestBody"
        },
        {
            "thread": self.thread,
            "author": None,
            "body": "TestBody"
        }]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    post = Post.objects.create(**test_case)
                    self.assertEqual(0, Post.objects.count())

class CommentsTest(TestCase):

    def setUp(self): 
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        self.user = User.objects.create_user(
            username="ExampleUser",
            email="User@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")

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
        self.group = Group.objects.create(name="TestGroup")
        self.forum = Forum.objects.create(shop=self.shop,
                                          title="TestTitle",
                                          description="TestDescription",
                                          threads=0,
                                          posts=0)
        self.forum.groups.add(self.group)
        self.thread = Thread.objects.create(forum=self.forum,
                                            title="TestTitle",
                                            posts=0,
                                            views=0,
                                            closed=False)
        self.post = Post.objects.create(thread=self.thread,
                                        author=self.user,
                                        body="TestBody")
    
    def test_comment_create(self): 
        comment = Comments.objects.create(from_user=self.user,
                                          post=self.post,
                                          body="TestBody")
        self.assertEqual(1, Comments.objects.count())
    
    def test_comments_create_null_values(self): 
        test_cases = [{
            "from_user": None, 
            "post": self.post,
            "body": "TestBody"
        },
        {
            "from_user": self.user, 
            "post": None,
            "body": "TestBody"
        }]

        for test_case in test_cases:
            with transaction.atomic():
                with self.assertRaises(IntegrityError):
                    comment = Comments.objects.create(**test_case)
                    self.assertEqual(0, Comments.objects.count())

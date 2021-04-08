from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Product, Category, Product, Producent, Assortment,\
                        Magazine, Shop
from ..forms import CreateForumForm, CreateThreadForm, CreatePostForm, CommentsForm
from ..models import Forum, Thread, Post
from django.contrib.auth.models import Group, User
from django.db import transaction


class CreateForumFormTest(TestCase): 

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
    
    
    def test_valid_forum_create(self): 
        data = {"groups": self.group,
                "shop": self.shop,
                "title": "TestTitle",
                "description": "TestDescription",
                "threads": 0,
                "posts": 0}
        form = CreateForumForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_forum_create(self): 
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
                form = CreateForumForm(data=test_case)
                self.assertFalse(form.is_valid())

class CreateThreadFormTest(TestCase): 

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

    def test_valid_thread_create(self): 
        data = {
            "forum": self.forum,
            "title": "TestThreadTitle",
            "posts": 0,
            "views": 0,
            "closed": False,
        }
        form = CreateThreadForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_thread_create(self): 
        test_cases = [{
            "forum": None, 
            "title": "TestTitle",
            "posts": 0,
            "views": 0,
            "closed": False
        },{
            "forum": self.forum,
            "title": None,
            "posts": 0,
            "views": 0,
            "closed": False
        }]

        for test_case in test_cases: 
            with transaction.atomic(): 
                form = CreateThreadForm(data=test_case)
                self.assertFalse(form.is_valid())

class CreatePostFormTest(TestCase): 

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
    
    def test_valid_post_create(self): 
        data = {
            "thread": self.thread,
            "author": self.user, 
            "body": "TestBody"
        }
        form = CreatePostForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_post_create(self): 
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
                form = CreatePostForm(data=test_case)
                self.assertFalse(form.is_valid())
    
class CreateCommentFormTest(TestCase): 

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
    
    def test_valid_comment_create(self): 
        data = {
            "from_user": self.user,
            "post": self.post,
            "body": "TestingBody"
        }
        form = CommentsForm(data=data)
        self.assertTrue(form.is_valid())

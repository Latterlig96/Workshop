from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Permission, Group
from shop.models import Producent, Category, Product, Assortment,\
                        Magazine, Shop, Owner, Employee
from django.shortcuts import reverse
from ..models import Forum, Thread, Post
from django.contrib.contenttypes.models import ContentType
from http import HTTPStatus

class ForumTest(TestCase):

    def setUp(self):
        
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploaded = SimpleUploadedFile('small.gif',
                                           small_gif, content_type='image/gif')
        self.owner_user = User.objects.create_user(
            username="ExampleUser",
            email="Owner@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")
        
        self.employee_user = User.objects.create_user(
            username="ExampleUser2",
            email="Employee@example.com",
            first_name="User",
            last_name="User-Surname",
            password="ExamplePassword")
        
        self.user_without_permissions = User.objects.create_user(
                                                                 username="NoneUser",
                                                                 email="Nani@example.com",
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
        self.owner = Owner.objects.create(owner=self.owner_user,
                                          shop=self.shop,
                                          has_ownership=True)

        self.employee = Employee.objects.create(shop=self.shop,
                                                employee=self.employee_user)

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
                                        author=self.employee_user,
                                        body="TestBody")

    def test_create_forum_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_create_forum", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("create_forum"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/create_forum.html')

    def test_create_forum_view_without_permissions(self): 
        login = self.client.login(username="ExampleUser2", password="ExamplePassword")
        response = self.client.get(reverse("create_forum"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/create_forum.html')
    
    def test_create_thread_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_create_thread", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("create_thread"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/create_thread.html')

    def test_create_thread_view_without_permissions(self): 
        login = self.client.login(username="NoneUser", password="ExamplePassword")
        response = self.client.get(reverse("create_thread"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/create_thread.html')

    def test_create_post_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_create_post", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/create_post.html')

    def test_create_post_view_without_permissions(self): 
        login = self.client.login(username="NoneUser", password="ExamplePassword")
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/create_post.html')

    def test_dashboard_forum_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_view_dashboard", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("forum_dashboard"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/forum_dashboard.html')

    def test_dashboard_forum_view_without_permissions(self): 
        login = self.client.login(username="ExampleUser2", password="ExamplePassword")
        response = self.client.get(reverse("forum_dashboard"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/forum_dashboard.html')
    
    def test_thread_list_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_view_thread", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("thread_list", kwargs={'id': self.forum.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/thread_list.html')

    def test_thread_list_view_without_permissions(self): 
        login = self.client.login(username="NoneUser", password="ExamplePassword")
        response = self.client.get(reverse("thread_list", kwargs={'id': self.forum.id}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/thread_list.html')

    def test_thread_detail_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_view_thread", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("thread_detail", kwargs={'id': self.thread.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/thread_detail.html')

    def test_thread_detail_view_without_permissions(self): 
        login = self.client.login(username="NoneUser", password="ExamplePassword")
        response = self.client.get(reverse("thread_detail", kwargs={'id': self.thread.id}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/thread_detail.html')
    
    def test_post_detail_view(self): 
        content_type = ContentType.objects.get_for_model(Owner)
        permission = Permission.objects.create(name="can_view_post", content_type=content_type)
        self.owner_user.user_permissions.add(permission)
        login = self.client.login(username="ExampleUser", password="ExamplePassword")
        response = self.client.get(reverse("post_detail", kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'forum/post_detail.html')

    def test_post_detail_view_without_permissions(self): 
        login = self.client.login(username="NoneUser", password="ExamplePassword")
        response = self.client.get(reverse("post_detail", kwargs={'id': self.post.id}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, 'forum/post_detail.html')

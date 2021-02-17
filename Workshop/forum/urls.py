from django.urls import path
from . import views


urlpatterns = [
    path('create/',
         views.create_forum,
         name="create_forum"),
    path('thread/create/',
         views.create_thread,
         name="create_thread"),
    path('post/create/',
         views.create_post,
         name="create_post"),
    path('dashboard/',
         views.forum_dashboard,
         name="forum_dashboard"),
    path('thread/list/<int:id>',
         views.thread_list,
         name="thread_list"),
    path('thread/detail/<int:id>',
         views.thread_detail,
         name="thread_detail"),
    path('post/detail/<int:id>',
         views.post_detail,
         name="post_detail")
]

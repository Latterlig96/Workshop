from django.contrib import admin
from .models import Forum, Post, Thread


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',
                    'threads', 'posts')
    filter_horizontal = ('groups', )


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'posts',
                    'views', 'closed')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'body')

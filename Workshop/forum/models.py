from django.contrib.auth.models import Group, User
from django.db import models
from shop.models import Shop


class Forum(models.Model):
    groups = models.ManyToManyField(Group,
                                    blank=True)
    shop = models.ForeignKey(Shop,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100,
                             null=False,
                             blank=False)
    description = models.TextField(null=False,
                                   blank=False)
    threads = models.IntegerField()
    posts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forum {self.title}"


class Thread(models.Model):
    forum = models.ForeignKey(Forum,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100,
                             blank=False,
                             null=False)
    posts = models.IntegerField()
    views = models.IntegerField()
    closed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread {self.title}"


class Post(models.Model):
    thread = models.ForeignKey(Thread,
                               on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post created by {self.author.first_name}"


class Comments(models.Model):
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name="comment_from_user")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment created by {self._from.first_name} to {self.to.first_name}"

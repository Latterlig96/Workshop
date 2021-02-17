from typing import Dict
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def set_username(sender: User,
                 instance: User,
                 **kwargs: Dict
                 ) -> None:
    if instance.username:
        try:
            username = instance.username
            counter: int = 1
            while User.objects.filter(username=username):
                username = instance.username + str(counter)
                counter += 1
            instance.username = username
        except User.DoesNotExist:
            instance.username = username

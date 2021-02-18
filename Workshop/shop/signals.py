from typing import Dict
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Employee, Owner

GROUPS = ('Employees', 'Owners')

PERMISSIONS = {
    'Employees': (
        'can_create_thread',
        'can_create_post',
        'can_resolve_order',
        'can_view_thread',
        'can_view_post'
    ),
    'Owners': (
        'can_create_forum',
        'can_create_thread',
        'can_create_post',
        'can_create_task',
        'can_delete_employee',
        'can_add_employee',
        'can_add_producent',
        'can_add_product',
        'can_add_magazine',
        'can_add_assortment',
        'can_add_category',
        'can_view_thread',
        'can_view_post'
        'can_delete_thread',
        'can_delete_post',
    )
}


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


@receiver(post_save, sender=Employee)
def create_group_permission_employee(sender: Employee,
                                     instance: Employee,
                                     **kwargs: Dict
                                     ) -> None:
    content_type = ContentType.objects.get_for_model(Employee)
    shop_name = instance.shop.name
    group, _ = Group.objects.get_or_create(
        name='_'.join((shop_name, GROUPS[0])))
    user = instance.employee
    user.groups.add(group)
    for _permission in PERMISSIONS['Employees']:
        permission, _ = Permission.objects.get_or_create(codename=_permission,
                                                         name=" ".join(
                                                             _permission.split("_")),
                                                         content_type=content_type)
        group.permissions.add(permission)


@receiver(post_save, sender=Owner)
def create_group_permission_owner(sender: Owner,
                                  instance: Owner,
                                  **kwargs: Dict
                                  ) -> None:
    content_type = ContentType.objects.get_for_model(Owner)
    shop_name = instance.shop.name
    group, _ = Group.objects.get_or_create(
        name='_'.join((shop_name, GROUPS[1])))
    user = instance.owner
    user.groups.add(group)
    for _permission in PERMISSIONS['Owners']:
        permission, _ = Permission.objects.get_or_create(codename=_permission,
                                                         name=" ".join(
                                                             _permission.split("_")),
                                                         content_type=content_type)
        group.permissions.add(permission)

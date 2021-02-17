from django import template
from ..models import Employee, Owner

register = template.Library()


@register.filter
def is_employee(user: str) -> bool:
    employee = Employee.objects.filter(employee=user).exists()
    if employee:
        return True
    return False


@register.filter
def is_owner(user: str) -> bool:
    owner = Owner.objects.filter(owner=user).exists()
    if owner:
        return True
    return False

from typing import Dict
from shop.models import Employee, Owner


def create_username_from_email(cleaned_data: Dict) -> str:
    return cleaned_data["email"].split("@")[0]


def is_employee(user: str) -> bool:
    employee = Employee.objects.filter(employee=user).exists()
    if employee:
        return True
    return False


def is_owner(user: str) -> bool:
    owner = Owner.objects.filter(owner=user).exists()
    if owner:
        return True
    return False

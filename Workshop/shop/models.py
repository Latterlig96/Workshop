from django.contrib.auth.models import User
from django.db import models


class Producent(models.Model):
    logo = models.ImageField(blank=True,
                             null=True,
                             upload_to="media/")
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            primary_key=True)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    category_logo = models.ImageField(blank=True,
                                      null=True,
                                      upload_to="media/")
    name = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            primary_key=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    logo = models.ImageField(blank=True,
                             null=True,
                             upload_to="media/")
    name = models.CharField(max_length=50,
                            blank=False,
                            null=False,
                            unique=True)
    price = models.FloatField(blank=False,
                              null=False)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Product with name {self.name}"


class Assortment(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False,
                                   null=False)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f"Assortment for {self.product}"


class Magazine(models.Model):
    address = models.CharField(max_length=50,
                               blank=False,
                               null=False)
    assortment = models.ManyToManyField(Assortment)

    def __str__(self):
        return f"Magazine placed at {self.address}"


class Shop(models.Model):
    name = models.CharField(max_length=50,
                            blank=False,
                            null=False,
                            unique=True)
    producent = models.ManyToManyField(Producent)
    address = models.CharField(max_length=50,
                               blank=False)
    magazine = models.ManyToManyField(Magazine)

    def __str__(self):
        return f"{self.name}"


class Employee(models.Model):
    shop = models.ForeignKey(Shop,
                             on_delete=models.CASCADE)
    employee = models.ForeignKey(User,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}"


class EmployeeProfile(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField()

    def __str__(self):
        return f"Profile of a {self.employee.username}"


class Owner(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop,
                             on_delete=models.CASCADE)
    has_ownership = models.BooleanField()

    def __str__(self):
        return f"Owner of a shop {self.shop.name}"


class OwnerProfile(models.Model):
    owner = models.ForeignKey(Owner,
                              on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField()

    def __str__(self):
        return f"Profile of a {self.owner.username}"


class Task(models.Model):

    STATUS = (
        ('assigned', "Task assigned"),
        ('In Progress', "Task in progress"),
        ('Solved', "Task solved"),
    )

    task_from = models.ForeignKey(Owner,
                                  on_delete=models.CASCADE)
    task_to = models.ForeignKey(Employee,
                                on_delete=models.CASCADE)
    status = models.CharField(max_length=30,
                              choices=STATUS)
    description = models.TextField()
    execution_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task from {self.task_from} to {self.task_to}"

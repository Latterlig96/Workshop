from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Assortment, Category, Employee, EmployeeProfile, Magazine, Owner, Producent, Product, Shop, Task


class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class MyUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass


class EmailRequiredUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    add_fieldsets = ((None, {
        'fields': ('first_name', 'last_name',
                   'username', 'email',
                   'password1', 'password2'),
        'classes': ('wide',)
    }),)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Producent)
class ProducentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_logo', 'name')


@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'category')


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('address',)
    filter_horizontal = ('assortment',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    filter_horizontal = ('producent', 'magazine')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('shop', 'employee')


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'image')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'shop', 'has_ownership')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_from', 'task_to',
                    'description', 'execution_time')


admin.site.unregister(User)
admin.site.register(User, EmailRequiredUserAdmin)

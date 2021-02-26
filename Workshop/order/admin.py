from django.contrib import admin
from .models import OrderInformation, OrderItem


@admin.register(OrderInformation)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'address',
                    'city', 'zipcode', 'created_at')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)
    list_display = ('quantity', 'created_at',
                    'order_information', 'shop')

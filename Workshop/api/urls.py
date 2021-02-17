from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('product/list',
         views.ProductList.as_view(),
         name="api_product_list"),
    path('product/<int:pk>',
         views.ProductDetail.as_view(),
         name="api_product_detail"),
    path('customer/register/',
         views.RegisterCustomer.as_view(),
         name="api_customer_register"),
    path('employee/list',
         views.EmployeeList.as_view(),
         name="api_employee_list"),
    path('employee/<int:pk>',
         views.EmployeeDetail.as_view(),
         name="api_employee_detail"),
    path('order/create/<str:product>',
         views.OrderListOrCreate.as_view(),
         name="api_order_create")
]

urlpatterns = format_suffix_patterns(urlpatterns)

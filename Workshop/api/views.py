from typing import Dict
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404
from order.models import OrderInformation, OrderItem
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Employee, Product, Shop
from .serializers import EmployeeSerializer, OrderInformationSerializer, ProductSerializer, RegisterCustomerSerializer


class ProductList(APIView):

    def get(self,
            request: WSGIRequest,
            format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):

    def get(self,
            request: WSGIRequest,
            pk: int,
            format=None):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class RegisterCustomer(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterCustomerSerializer


class EmployeeList(APIView):

    def get(self,
            request: WSGIRequest,
            format=None):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeDetail(APIView):

    def get(self,
            request: WSGIRequest,
            pk: int,
            format=None):

        employee = get_object_or_404(Employee, id=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class OrderListOrCreate(APIView):

    def get(self,
            request: WSGIRequest,
            product: str):
        product = Product.objects.get(name=product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self,
             request,
             product: str,
             format=None):
        serializer = OrderInformationSerializer(data=request.data)
        product = Product.objects.get(name=product)
        shop = Shop.objects.get(magazine__assortment__product=product)
        if serializer.is_valid():
            data: Dict = serializer.data
            order_information = OrderInformation.objects.create(name=data['name'],
                                                                surname=data['surname'],
                                                                email=data['email'],
                                                                address=data['address'],
                                                                city=data['city'],
                                                                zipcode=data['zipcode'])
            OrderItem.objects.create(product=product,
                                     quantity=1,
                                     order_information=order_information,
                                     shop=shop)

            return Response("Order have been successfully created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

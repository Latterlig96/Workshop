from typing import Dict
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from customer.models import Customer
from order.models import OrderInformation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from shop.models import Employee, Product


class RegisterCustomerSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True,
                                    required=True)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True,
                                      required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'address',
                  'password', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs: Dict):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data: Dict):
        user = User.objects.create(
            username=validated_data['email'].split("@")[0],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'])
        Customer.objects.create(customer=user,
                                address=validated_data['address'])
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    employee = serializers.RelatedField(read_only=True)
    shop = serializers.RelatedField(read_only=True)

    class Meta:
        model = Employee
        fields = ('employee', 'shop')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price',
                  'category', 'description')


class OrderInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInformation
        fields = ('name', 'surname',
                  'email', 'address',
                  'city', 'zipcode')

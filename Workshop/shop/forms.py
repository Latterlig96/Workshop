from typing import Dict
from django import forms
from django.contrib.auth.models import User
from .models import Assortment, Category, Magazine, Producent,\
                    Product, Shop, Task, NewEmployee


class EmployeeRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    shop = forms.ModelChoiceField(queryset=Shop.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name')

    def clean_confirm_password(self):
        cd: Dict = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(cd['password']) < 8:
            raise forms.ValidationError(
                'Password length must be at least 8 letters')
        return cd['confirm_password']

    def clean_email(self):
        cd: Dict = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(f"Email: {cd['email']} already exists")
        return cd['email']


class OwnerLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    shop = forms.ModelChoiceField(queryset=Shop.objects.all())

    class Meta:
        model = User
        fields = ('email',)


class EmployeeLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)


class EmployeeEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class OwnerEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProducentRegisterForm(forms.ModelForm):
    class Meta:
        model = Producent
        fields = '__all__'


class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryRegisterForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AssortmentRegisterForm(forms.ModelForm):
    class Meta:
        model = Assortment
        fields = '__all__'


class MagazineRegisterForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = '__all__'

class NewEmployeeRegisterForm(forms.ModelForm):
    class Meta: 
        model = NewEmployee
        fields = '__all__'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class TaskStatusForm(forms.ModelForm): 
    status = forms.ChoiceField(choices=Task.STATUS,
                               required=True)
    class Meta: 
        model = Task
        fields = ('status',)

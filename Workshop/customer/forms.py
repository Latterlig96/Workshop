from typing import Dict
from django import forms
from django.contrib.auth.models import User


class CustomerRegisterForm(forms.ModelForm):
    address = forms.CharField(max_length=100,
                              required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name')

    def clean_confirm_password(self):
        cd: Dict = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(cd['password']) < 8: 
            raise forms.ValidationError('Password length must be at least 8 letters')
        return cd['confirm_password']
    
    def clean_email(self):
        cd: Dict = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(f"Email: {cd['email']} already exists")
        return cd['email']

class CustomerLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)


class CustomerEditForm(forms.ModelForm):
    address = forms.CharField(max_length=100,
                              required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

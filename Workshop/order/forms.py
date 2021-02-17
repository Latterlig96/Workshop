from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import OrderInformation


class OrderInformationForm(ModelForm):
    class Meta:
        model = OrderInformation
        fields = ('name', 'surname',
                  'email', 'address',
                  'city', 'zipcode')

    def clean_email(self):
        cd = self.cleaned_data
        if not User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError(
                f"Email: {cd['email']} does not exists")
        return cd['email']

from http import HTTPStatus
from typing import Dict
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .forms import CustomerEditForm, CustomerLoginForm, CustomerRegisterForm
from .models import Customer, CustomerProfile
from .utils import create_username_from_email


def register(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        customer_form = CustomerRegisterForm(request.POST)
        if customer_form.is_valid():
            cd: Dict = customer_form.cleaned_data
            user = User.objects.create_user(username=create_username_from_email(cd),
                                            email=cd["email"],
                                            password=cd["password"],
                                            first_name=cd["first_name"],
                                            last_name=cd["last_name"])
            Customer.objects.create(customer=user,
                                    address=cd['address'])

            template = render_to_string('customer/email_template.html',
                                        context={'name': user.first_name})
            email = EmailMessage(
                'Registration success',
                template,
                settings.EMAIL_HOST_USER,
                [user.email])
            email.fail_silently = False
            email.send()

            return render(request,
                          'customer/register_done.html',
                          {'customer': cd},
                          status=HTTPStatus.OK)
    else:
        customer_form = CustomerRegisterForm()
    return render(request,
                  'customer/register.html',
                  {'form': customer_form},
                  status=HTTPStatus.OK)


def log_in(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            cd: Dict = form.cleaned_data
            try:
                customer = Customer.objects.get(customer__email=cd['email'])
            except Customer.DoesNotExist:
                messages.error(request, "Invalid login or password")
                return render(request,
                              'customer/login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)

            customer = authenticate(request,
                                    username=customer.customer.username,
                                    password=cd['password'])
            if customer is not None:
                if customer.is_active:
                    login(request, customer)
                    return redirect('dashboard')
                messages.error(request, "Your account has been disabled")
                return render(request,
                              'customer/login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)
    else:
        form = CustomerLoginForm()
    return render(request,
                  'customer/login.html',
                  {'form': form},
                  status=HTTPStatus.OK)


@login_required
def customer_settings(request: WSGIRequest) -> HttpResponse:
    customer = Customer.objects.get(customer=request.user)
    return render(request,
                  'customer/settings.html',
                  {'customer': customer},
                  status=HTTPStatus.OK)


@login_required
def edit(request: WSGIRequest) -> HttpResponse:
    customer = Customer.objects.get(customer=request.user)
    if request.method == 'POST':
        customer_form = CustomerEditForm(instance=customer.customer,
                                         files=request.FILES,
                                         data=request.POST)
        if customer_form.is_valid():
            cd: Dict = customer_form.cleaned_data
            customer_form = customer_form.save(commit=False)
            CustomerProfile.objects.create(customer=customer,
                                           phone_number=cd['phone_number'],
                                           image=cd['image'])
            customer_form.save()
            messages.success(
                request, "Your account has been updated successfully")
            return redirect('customer_settings')

    initial_data = {"address": customer.address,
                    "email": customer.customer.email}
    customer_form = CustomerEditForm(instance=customer.customer,
                                     initial=initial_data)
    return render(request,
                  'customer/edit_profile.html',
                  {'form': customer_form},
                  status=HTTPStatus.OK)

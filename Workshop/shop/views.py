from http import HTTPStatus
from typing import Dict, List
from itertools import product
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from cart.cart import Cart
from cart.forms import CartAddProductForm
from order.forms import OrderInformationForm
from order.models import OrderInformation, OrderItem
from django.db.models import ProtectedError
from .filters import ProductFilter
from .forms import AssortmentRegisterForm, CategoryRegisterForm, EmployeeEditForm, EmployeeLoginForm, \
    EmployeeRegisterForm, MagazineRegisterForm, OwnerEditForm, OwnerLoginForm, ProducentRegisterForm, \
    ProductRegisterForm, TaskForm, TaskStatusForm, NewEmployeeRegisterForm
from .models import Assortment, Category, Employee, EmployeeProfile, Magazine, Owner, OwnerProfile, Producent, \
    Product, Shop, Task, NewEmployee
from .utils import create_username_from_email, is_employee, is_owner


def register(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        employee_form = EmployeeRegisterForm(request.POST)
        if employee_form.is_valid():
            cd: Dict = employee_form.cleaned_data
            if NewEmployee.objects.filter(email=cd['email']).exists():
                user = User.objects.create_user(username=create_username_from_email(cd),
                                            email=cd["email"],
                                            password=cd["password"],
                                            first_name=cd["first_name"],
                                            last_name=cd["last_name"])
                Employee.objects.create(employee=user,
                                        shop=cd['shop'])
                NewEmployee.objects.get(email=cd['email']).delete()
                template = render_to_string('shop/employee/email_template.html',
                                            context={'name': user.first_name})
                email = EmailMessage(
                    'Registration success',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user.email])
                email.fail_silently = False
                email.send()
                return render(request,
                            'shop/employee/register_done.html',
                            {'form': cd},
                            status=HTTPStatus.OK)
            return render(request,
                          'errors/register_error.html',
                          status=HTTPStatus.NOT_FOUND)
    else:
        employee_form = EmployeeRegisterForm()
    return render(request,
                  'shop/employee/register.html',
                  {'form': employee_form},
                  status=HTTPStatus.OK)


def log_in(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            cd: Dict = form.cleaned_data
            try:
                employee = Employee.objects.get(employee__email=cd['email'])
            except Employee.DoesNotExist:
                messages.error(request, "Invalid login or password")
                return render(request,
                              'shop/employee/login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)

            employee = authenticate(request,
                                    username=employee.employee.username,
                                    password=cd['password'])
            if employee is not None:
                if employee.is_active:
                    login(request, employee)
                    return redirect('employee_dashboard')
                messages.error(request, "Your account has been disabled")
                return render(request,
                              'shop/employee/login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)
    else:
        form = EmployeeLoginForm()
    return render(request,
                  'shop/employee/login.html',
                  {'form': form},
                  status=HTTPStatus.OK)


def owner_log_in(request: WSGIRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            cd: Dict = form.cleaned_data
            try:
                owner = Owner.objects.get(owner__email=cd['email'],
                                          shop=cd['shop'])
            except Owner.DoesNotExist:
                messages.error(request, "Invalid login or password")
                return render(request,
                              'shop/owner/owner_login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)

            owner = authenticate(request,
                                 username=owner.owner.username,
                                 password=cd['password'])
            if owner is not None:
                if owner.is_active:
                    login(request, owner)
                    return redirect('owner_dashboard')
                messages.error(request, "Your account has been disabled")
                return render(request,
                              'shop/owner/owner_login.html',
                              {'form': form},
                              status=HTTPStatus.SEE_OTHER)
    else:
        form = OwnerLoginForm()
    return render(request,
                  'shop/owner/owner_login.html',
                  {'form': form},
                  status=HTTPStatus.OK)


def index(request: WSGIRequest) -> HttpResponse:
    return render(request,
                  'shop/index.html',
                  status=HTTPStatus.OK)


@login_required
def dashboard(request: WSGIRequest) -> HttpResponse:
    filter = ProductFilter(request.GET, queryset=Product.objects.all())
    producents = Producent.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    cart_product_form = CartAddProductForm()
    name = request.GET.get("name")
    if name:
        return redirect('products_list', filter=name)
    return render(request,
                  'shop/dashboard.html',
                  {'filter': filter,
                   'producents': producents,
                   'categories': categories,
                   'products:': products,
                   'cart_product_form': cart_product_form},
                  status=HTTPStatus.OK)


@login_required
def product_detail(request: WSGIRequest,
                   name: str
                   ) -> HttpResponse:
    product = get_object_or_404(Product, name=name)
    return render(request,
                  'shop/product_detail.html',
                  {'product': product},
                  status=HTTPStatus.OK)


@login_required
def product_order(request: WSGIRequest,
                  product: str
                  ) -> HttpResponse:
    if request.method == "POST":
        order_form = OrderInformationForm(request.POST)
        product = Product.objects.get(name=product)
        shop = Shop.objects.filter(magazine__assortment__product=product).first()
        if order_form.is_valid():
            cd: Dict = order_form.cleaned_data
            order_info = OrderInformation.objects.create(name=cd['name'],
                                                         surname=cd['surname'],
                                                         email=cd['email'],
                                                         address=cd['address'],
                                                         city=cd['city'],
                                                         zipcode=cd['zipcode'])
            order_item = OrderItem.objects.create(product=product,
                                                  quantity=1,
                                                  order_information=order_info,
                                                  shop=shop)
            return render(request,
                          'order/order_done.html',
                          {'user': request.user},
                          status=HTTPStatus.OK)
    else:
        product = Product.objects.get(name=product)
        order_form = OrderInformationForm()
        return render(request,
                      'order/create_order.html',
                      {'form': order_form,
                       'product': product},
                      status=HTTPStatus.OK)

@login_required
def product_order_from_checkout(request: WSGIRequest) -> HttpResponse:
    cart = Cart(request)
    products: List[Product] = [] 
    quantities: List[int] = []
    if not cart.cart: 
        return render(request,
                      'cart/cart_empty.html',
                      status=HTTPStatus.NOT_FOUND)
    for item in cart: 
        products.append(item['product'])
        quantities.append(item['quantity'])
    if request.method == "POST":
        order_form = OrderInformationForm(request.POST)
        if order_form.is_valid(): 
            cd: Dict = order_form.cleaned_data
            order_info = OrderInformation.objects.create(name=cd['name'],
                                                         surname=cd['surname'],
                                                         email=cd['email'],
                                                         address=cd['address'],
                                                         city=cd['city'],
                                                         zipcode=cd['zipcode'])
            for product, quantity in zip(products, quantities):
                shop = Shop.objects.filter(magazine__assortment__product=product).first()
                OrderItem.objects.create(product=product,
                                         quantity=quantity,
                                         order_information=order_info,
                                         shop=shop)
            return render(request,
                        'order/order_done.html',
                        {'user': request.user},
                        status=HTTPStatus.OK)
    else: 
        order_form = OrderInformationForm()
    return render(request,
                      'order/create_order_from_checkout.html',
                      {'form': order_form,
                       'products': products},
                      status=HTTPStatus.OK)


@login_required
def order_list(request: WSGIRequest) -> HttpResponse:
    employee = Employee.objects.get(employee=request.user)
    order_items = OrderItem.objects.filter(shop=employee.shop).all()
    return render(request,
                  'order/orders_list.html',
                  {'items': order_items},
                  status=HTTPStatus.OK)


@login_required
def order_detail(request: WSGIRequest,
                 id: int) -> HttpResponse:
    order = OrderInformation.objects.get(pk=id)
    order_items = OrderItem.objects.filter(order_information=order).all()
    return render(request,
                  'order/order_detail.html',
                  {'order': order,
                   'order_items': order_items},
                  status=HTTPStatus.OK)

@login_required 
def order_magazine_check(request: WSGIRequest,
                         id: int) -> HttpResponse: 
    employee = Employee.objects.get(employee=request.user)
    shop = Shop.objects.get(id=employee.shop.id)
    magazines = [magazine for magazine in shop.magazine.iterator()]
    return render(request,
                  'order/order_magazine_check.html',
                  {'magazines': magazines},
                  status=HTTPStatus.OK)

@login_required 
def order_resolve(request: WSGIRequest, 
                  id: int) -> HttpResponse: 
    employee = Employee.objects.get(employee=request.user)
    shop = Shop.objects.get(id=employee.shop.id)
    order = OrderInformation.objects.get(pk=id)
    order_items = OrderItem.objects.filter(order_information=order).all()
    magazines = [magazine for magazine in shop.magazine.iterator()]

    for order_item, magazine in product(order_items, magazines): 
        if magazine.assortment.filter(product=order_item.product).exists():
            if order_item.quantity == 0: 
                continue 
            magazine_assortment = magazine.assortment.filter(product=order_item.product).first()
            assortment_quantity = magazine_assortment.quantity   
            if assortment_quantity > order_item.quantity:
                assortment_quantity -= order_item.quantity
                magazine_assortment.quantity = assortment_quantity 
                order_item.quantity = 0 
                order_item.save()
                magazine_assortment.save() 

    for order_item in order_items:
        if order_item.quantity == 0: 
            order_item.delete()     
    messages.success(request, "Order has been sucessfully resolved")
    return redirect('order_list')


@login_required
def product_filter_list(request: WSGIRequest,
                        filter: str
                        ) -> HttpResponse:
    products = Product.objects.filter(name__icontains=filter).all()
    cart_product_form = CartAddProductForm()
    if products.exists():
        return render(request,
                      'shop/products_list.html',
                      {'products': products,
                       'cart_product_form': cart_product_form},
                      status=HTTPStatus.OK)
    messages.error(request, "No products found")
    return redirect('dashboard')


@login_required
def category_products_filter_list(request: WSGIRequest,
                                  category: str
                                  ) -> HttpResponse:
    products = Product.objects.filter(category__name=category).all()
    cart_product_form = CartAddProductForm()
    if products.exists():
        return render(request,
                      'shop/products_list.html',
                      {'products': products,
                       'cart_product_form': cart_product_form},
                      status=HTTPStatus.OK)
    messages.error(request, "No products found")
    return redirect('dashboard')


@login_required
def producent_products_filter_list(request: WSGIRequest,
                                   producent: str
                                   ) -> HttpResponse:
    shops = Shop.objects.filter(producent=producent).all()
    products = []
    cart_product_form = CartAddProductForm()
    for shop in shops.iterator():
        for magazine in shop.magazine.iterator():
            for assortment in magazine.assortment.iterator():
                products.append(assortment.product)
    
    if products:
        return render(request,
                    'shop/products_list.html',
                    {'products': products,
                    'cart_product_form': cart_product_form},
                    status=HTTPStatus.OK)

    messages.error(request, "No products found from given producent")
    return redirect('dashboard')

@login_required
def employee_settings(request: WSGIRequest) -> HttpResponse:
    if not is_employee(request.user):
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    employee = Employee.objects.get(employee=request.user)
    try:
        employee_profile = EmployeeProfile.objects.get(employee=employee)
    except EmployeeProfile.DoesNotExist: 
        employee_profile = None

    return render(request,
                  'shop/employee/employee_settings.html',
                  {'employee': employee,
                   'employee_profile': employee_profile},
                  status=HTTPStatus.OK)


@login_required
def owner_settings(request: WSGIRequest) -> HttpResponse:
    if not is_owner(request.user): 
        return render(request, 
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    owner = Owner.objects.get(owner=request.user)
    try: 
        owner_profile = OwnerProfile.objects.get(owner=owner)
    except OwnerProfile.DoesNotExist: 
        owner_profile = None
        
    return render(request,
                  'shop/owner/owner_settings.html',
                  {'owner': owner,
                   'owner_profile': owner_profile},
                  status=HTTPStatus.OK)


@login_required
def employee_dashboard(request: WSGIRequest) -> HttpResponse:
    if not is_employee(request.user): 
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    return render(request,
                  'shop/employee/employee_dashboard.html',
                  status=HTTPStatus.OK)


@login_required
def employee_edit(request: WSGIRequest) -> HttpResponse:
    if not is_employee(request.user): 
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    employee = Employee.objects.get(employee=request.user)
    if request.method == 'POST':
        employee_form = EmployeeEditForm(instance=employee.employee,
                                         files=request.FILES,
                                         data=request.POST)
        if employee_form.is_valid():
            cd: Dict = employee_form.cleaned_data
            if EmployeeProfile.objects.filter(employee=employee).exists():
                employee_profile = EmployeeProfile.objects.get(
                    employee=employee)
                employee_profile.phone_number = cd['phone_number']
                employee_profile.image = cd['image']
                employee_profile.save()
            else:
                EmployeeProfile.objects.create(employee=employee,
                                               phone_number=cd['phone_number'],
                                               image=cd['image'])
            messages.success(
                request, "Your account has been updated successfully")
            return redirect('employee_settings')
    else:
        initial_data = {"email": employee.employee.email,
                        "first_name": employee.employee.first_name,
                        "last_name": employee.employee.last_name}
        employee_form = EmployeeEditForm(instance=employee.employee,
                                         initial=initial_data)
    return render(request,
                  'shop/employee/edit_profile.html',
                  {'form': employee_form},
                  status=HTTPStatus.OK)


@login_required
def owner_edit(request: WSGIRequest) -> HttpResponse:
    if not is_owner(request.user): 
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    owner = Owner.objects.get(owner=request.user)
    if request.method == 'POST':
        owner_form = OwnerEditForm(instance=owner.owner,
                                   files=request.FILES,
                                   data=request.POST)
        if owner_form.is_valid():
            cd: Dict = owner_form.cleaned_data
            if OwnerProfile.objects.filter(owner=owner).exists():
                owner_profile = OwnerProfile.objects.get(owner=owner)
                owner_profile.phone_number = cd['phone_number']
                owner_profile.image = cd['image']
                owner_profile.save()
            else:
                OwnerProfile.objects.create(owner=owner,
                                            phone_number=cd['phone_number'],
                                            image=cd['image'])
            messages.success(
                request, "Your account has been updated successfully")
            return redirect('owner_settings')
    else:
        initial_data = {"email": owner.owner.email,
                        "first_name": owner.owner.first_name,
                        "last_name": owner.owner.last_name}
        owner_form = OwnerEditForm(instance=owner.owner,
                                   initial=initial_data)
    return render(request,
                  'shop/owner/edit_profile.html',
                  {'form': owner_form},
                  status=HTTPStatus.OK)


@login_required
def owner_dashboard(request: WSGIRequest) -> HttpResponse:
    if not is_owner(request.user):
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    owner = Owner.objects.get(owner=request.user)
    return render(request,
                  'shop/owner/owner_dashboard.html',
                  {'owner': owner},
                  status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_add_producent')
def register_new_producent(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        producent_form = ProducentRegisterForm(request.POST,
                                               request.FILES)
        if producent_form.is_valid():
            cd: Dict = producent_form.cleaned_data
            Producent.objects.create(logo=cd['logo'],
                                     name=cd['name'])
            messages.success(
                request, "New Producent has been added to your shop")
            return redirect('owner_dashboard')
    else:
        producent_form = ProducentRegisterForm()
        return render(request,
                      'shop/owner/register_producent.html',
                      {'form': producent_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_add_product')
def register_new_product(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        product_form = ProductRegisterForm(request.POST,
                                           request.FILES)
        if product_form.is_valid():
            cd: Dict = product_form.cleaned_data
            Product.objects.create(logo=cd['logo'],
                                   name=cd['name'],
                                   price=cd['price'],
                                   category=cd['category'],
                                   description=cd['description'])
            messages.success(
                request, "New Product has been added to your shop")
            return redirect('owner_dashboard')
    else:
        product_form = ProductRegisterForm()
        return render(request,
                      'shop/owner/register_product.html',
                      {'form': product_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_add_category')
def register_new_category(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        category_form = CategoryRegisterForm(request.POST,
                                             request.FILES)
        if category_form.is_valid():
            cd: Dict = category_form.cleaned_data
            Category.objects.create(category_logo=cd['category_logo'],
                                    name=cd['name'])
            messages.success(request, "New Category has been added")
            return redirect('owner_dashboard')
    else:
        category_form = CategoryRegisterForm()
        return render(request,
                      'shop/owner/register_category.html',
                      {'form': category_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_add_assortment')
def register_new_assortment(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        assortment_form = AssortmentRegisterForm(request.POST)
        if assortment_form.is_valid():
            cd: Dict = assortment_form.cleaned_data
            Assortment.objects.create(product=cd['product'],
                                      quantity=cd['quantity'],
                                      category=cd['category'])
            messages.success(
                request, "New Assortment has been added to your shop")
            return redirect('owner_dashboard')
    else:
        assortment_form = AssortmentRegisterForm()
        return render(request,
                      'shop/owner/register_assortment.html',
                      {'form': assortment_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_add_magazine')
def register_new_magazine(request: WSGIRequest) -> HttpResponse:
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    if request.method == "POST":
        magazine_form = MagazineRegisterForm(request.POST)
        if magazine_form.is_valid():
            cd: Dict = magazine_form.cleaned_data
            new_magazine = Magazine.objects.create(address=cd['address'])
            new_magazine.assortment.add(*cd['assortment'])
            shop.magazine.add(new_magazine)
            messages.success(
                request, "New Magazine has been added to your shop")
            return redirect('owner_dashboard')
    else:
        magazine_form = MagazineRegisterForm()
        return render(request,
                      'shop/owner/register_magazine.html',
                      {'form': magazine_form},
                      status=HTTPStatus.OK)

@login_required
@permission_required('shop.can_add_employee')
def register_new_employee(request: WSGIRequest) -> HttpResponse: 
    if request.method == "POST":
        employee_form = NewEmployeeRegisterForm(request.POST)
        if employee_form.is_valid(): 
            cd: Dict = employee_form.cleaned_data 
            NewEmployee.objects.create(email=cd['email'])
            messages.success(request, "New employee email registered successfull")
            return redirect('owner_dashboard')
    else: 
        employee_form = NewEmployeeRegisterForm()
        return render(request,
                      'shop/owner/register_employee.html',
                      {'form': employee_form},
                      status=HTTPStatus.OK)

@login_required
@permission_required('shop.can_create_task')
def create_task(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            cd: Dict = task_form.cleaned_data
            Task.objects.create(task_from=cd['task_from'],
                                task_to=cd['task_to'],
                                status=cd['status'],
                                execution_time=cd['execution_time'])
            messages.success(request, "Task created successfully")
            return redirect('owner_dashboard')
    else:
        task_form = TaskForm()
        return render(request,
                      'shop/tasks/task_create.html',
                      {'form': task_form},
                      status=HTTPStatus.OK)


@login_required
@permission_required('shop.can_view_task')
def task_detail(request: WSGIRequest,
                id: int
                ) -> HttpResponse:
    task = Task.objects.get(id=id)
    if request.method == "POST":
        task_form = TaskStatusForm(request.POST)
        if task_form.is_valid(): 
            cd: Dict = task_form.cleaned_data
            task.status = cd['status']
            task.save()
            return render(request,
                  'shop/tasks/task_detail.html',
                  {'task': task,
                   'form': TaskStatusForm()},
                  status=HTTPStatus.OK)
    else: 
        task_form = TaskStatusForm()    
        return render(request,
                    'shop/tasks/task_detail.html',
                    {'task': task,
                     'form': task_form},
                    status=HTTPStatus.OK)

@login_required
@permission_required('shop.can_view_task')
def task_list(request: WSGIRequest) -> HttpResponse:
    if is_employee(request.user):
        employee = Employee.objects.get(employee=request.user)
        tasks = Task.objects.filter(task_to=employee).all()
    if is_owner(request.user):
        owner = Owner.objects.get(owner=request.user)
        tasks = Task.objects.filter(task_from=owner).all()
    return render(request,
                  'shop/tasks/task_list.html',
                  {'tasks': tasks},
                  status=HTTPStatus.OK)

@login_required
@permission_required('shop.can_view_employee_list')
def employee_list(request: WSGIRequest,
                  ) -> HttpResponse:
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    try:
        employees = Employee.objects.filter(shop__id=shop.id).all()
    except Employee.DoesNotExist: 
        employees = None
    return render(request,
                  'shop/owner/employee_list.html',
                  {'employees': employees},
                  status=HTTPStatus.OK)

@login_required 
@permission_required('shop.can_delete_employee')
def delete_employee(request: WSGIRequest,
                    id: int
                    ) -> HttpResponse: 
    employee = Employee.objects.get(id=id)
    try:
        employee.delete() 
    except ProtectedError: 
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    messages.success(request, "Employee deleted sucessfully")
    return redirect('employee_list') 

@login_required
@permission_required('shop.can_delete_producent')
def delete_producent(request: WSGIRequest,
                     name: str
                     ) -> HttpResponse:
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    try: 
        shop.producent.get(name=name).delete()
        shop.save()
    except ProtectedError:
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    messages.success(request, "Producent deleted sucessfully")
    return redirect('shop_assets') 

@login_required
@permission_required('shop.can_delete_producent')
def delete_producent(request: WSGIRequest,
                     name: str
                     ) -> HttpResponse:
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    try: 
        shop.producent.get(name=name).delete()
        shop.save()
    except ProtectedError:
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    messages.success(request, "Producent deleted sucessfully")
    return redirect('shop_assets') 
    
@login_required 
@permission_required('shop.can_delete_magazine')
def delete_magazine(request: WSGIRequest, 
                    address: str
                    ) -> HttpResponse: 
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    try: 
        shop.magazine.get(address=address).delete()
        shop.save()
    except ProtectedError:
        return render(request,
                      'errors/404.html',
                      status=HTTPStatus.NOT_FOUND)
    messages.success(request, "Magazine deleted sucessfully")
    return redirect('shop_assets') 

@login_required
@permission_required('shop.can_view_shop_assets')
def shop_assets(request: WSGIRequest) -> HttpResponse: 
    owner = Owner.objects.get(owner=request.user)
    shop = Shop.objects.get(name=owner.shop.name)
    return render(request, 
                  'shop/owner/shop_assets.html',
                  {'shop': shop},
                  status=HTTPStatus.OK)

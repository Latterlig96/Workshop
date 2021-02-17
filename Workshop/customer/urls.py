from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('login/',
         views.log_in,
         name='customer_login'),
    path('register/',
         views.register,
         name='customer_register'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('settings/',
         views.customer_settings,
         name="customer_settings"),
    path('edit/',
         views.edit,
         name="customer_edit"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]

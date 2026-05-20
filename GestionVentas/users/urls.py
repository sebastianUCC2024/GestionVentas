from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    ClienteRegisterView,
    VendedorRegisterView
)

urlpatterns = [

    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout'
    ),

    path(
        'registro/cliente/',
        ClienteRegisterView.as_view(),
        name='cliente_register'
    ),

    path(
        'registro/vendedor/',
        VendedorRegisterView.as_view(),
        name='vendedor_register'
    ),

]
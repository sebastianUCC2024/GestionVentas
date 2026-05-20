from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/usuarios/login/')),

    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
    path('ventas/', include('ventas.urls')),
    path('usuarios/', include('users.urls')),
    path('reportes/', include('reportes.urls')),
]
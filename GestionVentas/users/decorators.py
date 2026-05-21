from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol == 'ADMIN':
            return view_func(request, *args, **kwargs)

        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('ventas_dashboard')

    return wrapper


def vendedor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.rol in ['VENDEDOR', 'ADMIN']:
            return view_func(request, *args, **kwargs)

        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('ventas_dashboard')

    return wrapper
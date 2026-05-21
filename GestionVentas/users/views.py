from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import User
from .forms import ClienteRegistroForm, VendedorRegistroForm


class UserLoginView(DjangoLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.rol == User.Roles.CLIENTE:
            return reverse_lazy('cliente_list')

        if user.rol == User.Roles.VENDEDOR:
            return reverse_lazy('venta_list')

        if user.rol == User.Roles.ADMIN:
            return reverse_lazy('ventas_dashboard')

        return reverse_lazy('cliente_list')


class UserLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('login')


class ClienteRegisterView(CreateView):
    form_class = ClienteRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta de cliente creada correctamente.')
        return super().form_valid(form)


class VendedorRegisterView(CreateView):
    form_class = VendedorRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Cuenta de vendedor creada correctamente.')
        return super().form_valid(form)
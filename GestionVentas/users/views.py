from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import User
from .forms import ClienteRegistroForm, VendedorRegistroForm


class UserLoginView(DjangoLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.rol == User.Roles.CLIENTE:
            return reverse_lazy('cliente_dashboard')

        elif user.rol == User.Roles.VENDEDOR:
            return reverse_lazy('vendedor_dashboard')

        elif user.rol == User.Roles.ADMIN:
            return reverse_lazy('admin_dashboard')

        return reverse_lazy('login')


class UserLogoutView(DjangoLogoutView):
    template_name = 'users/logout.html'


class ClienteRegisterView(CreateView):
    form_class = ClienteRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class VendedorRegisterView(CreateView):
    form_class = VendedorRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
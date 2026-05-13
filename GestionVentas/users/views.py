from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ClienteRegistroForm, VendedorRegistroForm

# Create your views here.
class LoginView(LoginView):
    template_name = 'users/login.html'

class LogoutView(LogoutView):
    template_name = 'users/logout.html'

class ClienteRegisterView(CreateView):
    form_class = ClienteRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

class VendedorRegisterView(CreateView):
    form_class = VendedorRegistroForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')




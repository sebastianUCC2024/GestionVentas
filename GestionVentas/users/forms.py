from django.contrib.auth.forms import UserCreationForm
from .models import User

class ClienteRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = User.Roles.CLIENTE
        if commit:
            user.save()
        return user

class VendedorRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = User.Roles.VENDEDOR
        if commit:
            user.save()
        return user
    
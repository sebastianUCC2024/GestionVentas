from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        VENDEDOR = 'VENDEDOR', 'Vendedor'
        CLIENTE = 'CLIENTE', 'Cliente'

    rol = models.CharField(
        max_length=20,
        choices= Roles.choices,
        default= Roles.CLIENTE
    )

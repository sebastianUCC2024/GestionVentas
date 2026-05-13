from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'correo', 'telefono', 'estado', 'vendedor', 'fecha_registro')
    search_fields = ('nombre', 'documento', 'correo')
    list_filter = ('estado', 'fecha_registro')
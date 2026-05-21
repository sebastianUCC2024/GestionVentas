from django.contrib import admin
from .models import OportunidadVenta, Seguimiento


@admin.register(OportunidadVenta)
class OportunidadVentaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'cliente',
        'vendedor',
        'monto',
        'estado',
        'fecha_creacion',
        'fecha_cierre_estimada',
    )
    list_filter = ('estado', 'fecha_creacion', 'fecha_cierre_estimada')
    search_fields = (
        'titulo',
        'cliente__nombre',
        'cliente__documento',
        'vendedor__username',
    )
    ordering = ('-fecha_creacion',)


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'oportunidad',
        'usuario',
        'tipo_contacto',
        'fecha_contacto',
        'proximo_contacto',
        'completado',
    )
    list_filter = ('tipo_contacto', 'completado', 'fecha_contacto')
    search_fields = (
        'cliente__nombre',
        'oportunidad__titulo',
        'observaciones',
        'usuario__username',
    )
    ordering = ('-fecha_contacto',)

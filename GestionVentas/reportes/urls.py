from django.urls import path
from . import views

urlpatterns = [

    path(
        'clientes/pdf/',
        views.reporte_clientes_pdf,
        name='reporte_clientes_pdf'
    ),

    path(
        'ventas/excel/',
        views.reporte_ventas_excel,
        name='reporte_ventas_excel'
    ),

    path(
        'seguimientos/pdf/',
        views.reporte_seguimientos_pdf,
        name='reporte_seguimientos_pdf'
    ),

]
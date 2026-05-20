from django.urls import path
from . import views

urlpatterns = [
    path('', views.venta_list, name='venta_list'),
    path('dashboard/', views.ventas_dashboard, name='ventas_dashboard'),

    path('crear/', views.venta_create, name='venta_create'),
    path('<int:pk>/', views.venta_detail, name='venta_detail'),
    path('<int:pk>/editar/', views.venta_update, name='venta_update'),
    path('<int:pk>/eliminar/', views.venta_delete, name='venta_delete'),

    path('seguimientos/', views.seguimiento_list, name='seguimiento_list'),
    path('seguimientos/crear/', views.seguimiento_create, name='seguimiento_create'),
    path('seguimientos/<int:pk>/', views.seguimiento_detail, name='seguimiento_detail'),
    path('seguimientos/<int:pk>/editar/', views.seguimiento_update, name='seguimiento_update'),
    path('seguimientos/<int:pk>/eliminar/', views.seguimiento_delete, name='seguimiento_delete'),
    
    # APIs para datos de gráficos
    path('api/dashboard-data/', views.dashboard_data, name='dashboard_data'),
    
    # Exportación de reportes
    path('exportar/ventas/pdf/', views.exportar_ventas_pdf, name='exportar_ventas_pdf'),
    path('exportar/ventas/excel/', views.exportar_ventas_excel, name='exportar_ventas_excel'),
    path('exportar/clientes/pdf/', views.exportar_clientes_pdf, name='exportar_clientes_pdf'),
]
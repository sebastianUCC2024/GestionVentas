from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import json

# Importaciones para reportes
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

from clientes.models import Cliente
from .models import OportunidadVenta, Seguimiento
from .forms import OportunidadVentaForm, SeguimientoForm


@login_required
def venta_list(request):
    query = request.GET.get('q')
    estado = request.GET.get('estado')

    ventas = OportunidadVenta.objects.select_related(
        'cliente',
        'vendedor'
    ).all()

    if query:
        ventas = ventas.filter(
            Q(titulo__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__documento__icontains=query)
        )

    if estado:
        ventas = ventas.filter(estado=estado)

    total_ventas = ventas.count()
    total_monto = ventas.aggregate(total=Sum('monto'))['total'] or 0
    ventas_ganadas = ventas.filter(estado='ganada').count()
    ventas_perdidas = ventas.filter(estado='perdida').count()

    context = {
        'ventas': ventas,
        'query': query,
        'estado': estado,
        'total_ventas': total_ventas,
        'total_monto': total_monto,
        'ventas_ganadas': ventas_ganadas,
        'ventas_perdidas': ventas_perdidas,
    }

    return render(request, 'ventas/venta_list.html', context)


@login_required
def venta_detail(request, pk):
    venta = get_object_or_404(
        OportunidadVenta.objects.select_related('cliente', 'vendedor'),
        pk=pk
    )

    seguimientos = venta.seguimientos.select_related(
        'cliente',
        'usuario'
    ).all()

    return render(request, 'ventas/venta_detail.html', {
        'venta': venta,
        'seguimientos': seguimientos,
    })


@login_required
def venta_create(request):
    if request.method == 'POST':
        form = OportunidadVentaForm(request.POST)

        if form.is_valid():
            venta = form.save(commit=False)

            if not venta.vendedor:
                venta.vendedor = request.user

            venta.save()

            messages.success(
                request,
                'Oportunidad de venta creada correctamente.'
            )

            return redirect('venta_list')
    else:
        form = OportunidadVentaForm(initial={'vendedor': request.user})

    return render(request, 'ventas/venta_form.html', {'form': form})


@login_required
def venta_update(request, pk):
    venta = get_object_or_404(OportunidadVenta, pk=pk)

    if request.method == 'POST':
        form = OportunidadVentaForm(request.POST, instance=venta)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Oportunidad de venta actualizada correctamente.'
            )

            return redirect('venta_list')
    else:
        form = OportunidadVentaForm(instance=venta)

    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'venta': venta,
    })


@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(OportunidadVenta, pk=pk)

    if request.method == 'POST':
        venta.delete()

        messages.success(
            request,
            'Oportunidad de venta eliminada correctamente.'
        )

        return redirect('venta_list')

    return render(request, 'ventas/venta_confirm_delete.html', {
        'venta': venta
    })


@login_required
def seguimiento_list(request):
    query = request.GET.get('q')
    tipo = request.GET.get('tipo')

    seguimientos = Seguimiento.objects.select_related(
        'cliente',
        'oportunidad',
        'usuario'
    ).all()

    if query:
        seguimientos = seguimientos.filter(
            Q(cliente__nombre__icontains=query) |
            Q(oportunidad__titulo__icontains=query) |
            Q(observaciones__icontains=query)
        )

    if tipo:
        seguimientos = seguimientos.filter(tipo_contacto=tipo)

    total_seguimientos = seguimientos.count()
    pendientes = seguimientos.filter(completado=False).count()
    completados = seguimientos.filter(completado=True).count()

    context = {
        'seguimientos': seguimientos,
        'query': query,
        'tipo': tipo,
        'total_seguimientos': total_seguimientos,
        'pendientes': pendientes,
        'completados': completados,
    }

    return render(request, 'ventas/seguimiento_list.html', context)


@login_required
def seguimiento_detail(request, pk):
    seguimiento = get_object_or_404(
        Seguimiento.objects.select_related(
            'cliente',
            'oportunidad',
            'usuario'
        ),
        pk=pk
    )

    return render(request, 'ventas/seguimiento_detail.html', {
        'seguimiento': seguimiento
    })


@login_required
def seguimiento_create(request):
    if request.method == 'POST':
        form = SeguimientoForm(request.POST)

        if form.is_valid():
            seguimiento = form.save(commit=False)

            if not seguimiento.usuario:
                seguimiento.usuario = request.user

            seguimiento.save()

            messages.success(
                request,
                'Seguimiento registrado correctamente.'
            )

            return redirect('seguimiento_list')
    else:
        form = SeguimientoForm(initial={'usuario': request.user})

    return render(request, 'ventas/seguimiento_form.html', {
        'form': form
    })


@login_required
def seguimiento_update(request, pk):
    seguimiento = get_object_or_404(Seguimiento, pk=pk)

    if request.method == 'POST':
        form = SeguimientoForm(request.POST, instance=seguimiento)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Seguimiento actualizado correctamente.'
            )

            return redirect('seguimiento_list')
    else:
        form = SeguimientoForm(instance=seguimiento)

    return render(request, 'ventas/seguimiento_form.html', {
        'form': form,
        'seguimiento': seguimiento,
    })


@login_required
def seguimiento_delete(request, pk):
    seguimiento = get_object_or_404(Seguimiento, pk=pk)

    if request.method == 'POST':
        seguimiento.delete()

        messages.success(
            request,
            'Seguimiento eliminado correctamente.'
        )

        return redirect('seguimiento_list')

    return render(request, 'ventas/seguimiento_confirm_delete.html', {
        'seguimiento': seguimiento
    })


@login_required
def ventas_dashboard(request):
    total_clientes = Cliente.objects.count()
    total_ventas = OportunidadVenta.objects.count()

    total_ingresos = OportunidadVenta.objects.filter(
        estado='ganada'
    ).aggregate(total=Sum('monto'))['total'] or 0

    ventas_ganadas = OportunidadVenta.objects.filter(
        estado='ganada'
    ).count()

    ventas_perdidas = OportunidadVenta.objects.filter(
        estado='perdida'
    ).count()

    seguimientos = Seguimiento.objects.count()

    clientes_activos = Cliente.objects.filter(
        estado='activo'
    ).count()

    clientes_inactivos = Cliente.objects.filter(
        estado='inactivo'
    ).count()

    ventas_por_estado = (
        OportunidadVenta.objects
        .values('estado')
        .annotate(total=Count('id'))
    )

    ventas_recientes = (
        OportunidadVenta.objects
        .select_related('cliente')
        .order_by('-fecha_creacion')[:5]
    )

    context = {
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'total_ingresos': total_ingresos,
        'ventas_ganadas': ventas_ganadas,
        'ventas_perdidas': ventas_perdidas,
        'seguimientos': seguimientos,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
        'ventas_por_estado': ventas_por_estado,
        'ventas_recientes': ventas_recientes,
    }

    return render(request, 'ventas/ventas_dashboard.html', context)


# ============================================
# VISTAS PARA DATOS DE GRÁFICOS (AJAX/JSON)
# ============================================

@login_required
def dashboard_data(request):
    """
    Vista que retorna datos en JSON para los gráficos del dashboard
    """
    # Ventas por mes (últimos 6 meses)
    fecha_inicio = datetime.now() - timedelta(days=180)
    ventas_por_mes = (
        OportunidadVenta.objects
        .filter(fecha_creacion__gte=fecha_inicio)
        .annotate(mes=TruncMonth('fecha_creacion'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    
    ventas_mes_data = [
        {
            'mes': item['mes'].strftime('%b %Y') if item['mes'] else 'N/A',
            'total': item['total']
        }
        for item in ventas_por_mes
    ]

    # Ingresos por mes (últimos 6 meses)
    ingresos_por_mes = (
        OportunidadVenta.objects
        .filter(fecha_creacion__gte=fecha_inicio, estado='ganada')
        .annotate(mes=TruncMonth('fecha_creacion'))
        .values('mes')
        .annotate(total_ingresos=Sum('monto'))
        .order_by('mes')
    )
    
    ingresos_mes_data = [
        {
            'mes': item['mes'].strftime('%b %Y') if item['mes'] else 'N/A',
            'total_ingresos': float(item['total_ingresos'] or 0)
        }
        for item in ingresos_por_mes
    ]

    # Top 5 clientes con más ventas
    top_clientes = (
        Cliente.objects
        .annotate(total_ventas=Count('oportunidades'))
        .filter(total_ventas__gt=0)
        .order_by('-total_ventas')[:5]
    )
    
    top_clientes_data = [
        {
            'nombre': cliente.nombre,
            'total_ventas': cliente.total_ventas
        }
        for cliente in top_clientes
    ]

    # Ventas por estado
    ventas_por_estado = (
        OportunidadVenta.objects
        .values('estado')
        .annotate(total=Count('id'))
    )
    
    ventas_estado_data = [
        {
            'estado': item['estado'],
            'total': item['total']
        }
        for item in ventas_por_estado
    ]

    data = {
        'ventas_por_mes': ventas_mes_data,
        'ingresos_por_mes': ingresos_mes_data,
        'top_clientes': top_clientes_data,
        'ventas_por_estado': ventas_estado_data,
    }

    return JsonResponse(data)


# ============================================
# VISTAS PARA EXPORTACIÓN DE REPORTES
# ============================================

@login_required
def exportar_ventas_pdf(request):
    """
    Exporta reporte de ventas en formato PDF
    """
    # Crear buffer en memoria
    buffer = io.BytesIO()
    
    # Crear documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4e73df'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Título
    title = Paragraph("Reporte de Ventas - GestionVentas CRM", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fecha del reporte
    fecha_reporte = Paragraph(
        f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        styles['Normal']
    )
    elements.append(fecha_reporte)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen general
    total_ventas = OportunidadVenta.objects.count()
    ventas_ganadas = OportunidadVenta.objects.filter(estado='ganada').count()
    total_ingresos = OportunidadVenta.objects.filter(estado='ganada').aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    resumen_data = [
        ['Indicador', 'Valor'],
        ['Total de Ventas', str(total_ventas)],
        ['Ventas Ganadas', str(ventas_ganadas)],
        ['Ingresos Totales', f'${total_ingresos:,.2f}'],
    ]
    
    resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4e73df')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Tabla de ventas recientes
    subtitle = Paragraph("Ventas Recientes", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2*inch))
    
    ventas = OportunidadVenta.objects.select_related('cliente').order_by('-fecha_creacion')[:20]
    
    ventas_data = [['Cliente', 'Título', 'Monto', 'Estado']]
    for venta in ventas:
        ventas_data.append([
            venta.cliente.nombre[:20],
            venta.titulo[:30],
            f'${venta.monto:,.0f}',
            venta.get_estado_display()
        ])
    
    ventas_table = Table(ventas_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.2*inch])
    ventas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1cc88a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(ventas_table)
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_ventas_{datetime.now().strftime("%Y%m%d")}.pdf"'
    response.write(pdf)
    
    return response


@login_required
def exportar_ventas_excel(request):
    """
    Exporta reporte de ventas en formato Excel usando pandas
    """
    if not PANDAS_AVAILABLE:
        messages.error(request, 'La exportación a Excel no está disponible. Instale pandas.')
        return redirect('ventas_dashboard')
    
    # Obtener datos de ventas
    ventas = OportunidadVenta.objects.select_related('cliente', 'vendedor').all()
    
    # Crear DataFrame
    data = {
        'ID': [v.id for v in ventas],
        'Título': [v.titulo for v in ventas],
        'Cliente': [v.cliente.nombre for v in ventas],
        'Vendedor': [v.vendedor.username if v.vendedor else 'N/A' for v in ventas],
        'Monto': [float(v.monto) for v in ventas],
        'Estado': [v.get_estado_display() for v in ventas],
        'Fecha Creación': [v.fecha_creacion.strftime('%Y-%m-%d') for v in ventas],
        'Fecha Cierre': [v.fecha_cierre.strftime('%Y-%m-%d') if v.fecha_cierre else 'N/A' for v in ventas],
    }
    
    df = pd.DataFrame(data)
    
    # Crear archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Ventas', index=False)
        
        # Hoja de resumen
        resumen_data = {
            'Indicador': [
                'Total Ventas',
                'Ventas Ganadas',
                'Ventas Perdidas',
                'Ventas en Proceso',
                'Ingresos Totales'
            ],
            'Valor': [
                ventas.count(),
                ventas.filter(estado='ganada').count(),
                ventas.filter(estado='perdida').count(),
                ventas.filter(estado='en_proceso').count(),
                f"${ventas.filter(estado='ganada').aggregate(Sum('monto'))['monto__sum'] or 0:,.2f}"
            ]
        }
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
    
    output.seek(0)
    
    # Crear respuesta HTTP
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="reporte_ventas_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    
    return response


@login_required
def exportar_clientes_pdf(request):
    """
    Exporta reporte de clientes en formato PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#4e73df'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Título
    title = Paragraph("Reporte de Clientes - GestionVentas CRM", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fecha
    fecha_reporte = Paragraph(
        f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        styles['Normal']
    )
    elements.append(fecha_reporte)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(estado='activo').count()
    clientes_inactivos = Cliente.objects.filter(estado='inactivo').count()
    
    resumen_data = [
        ['Indicador', 'Cantidad'],
        ['Total Clientes', str(total_clientes)],
        ['Clientes Activos', str(clientes_activos)],
        ['Clientes Inactivos', str(clientes_inactivos)],
    ]
    
    resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#36b9cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(resumen_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Lista de clientes
    subtitle = Paragraph("Lista de Clientes", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2*inch))
    
    clientes = Cliente.objects.all()[:30]
    
    clientes_data = [['Nombre', 'Documento', 'Email', 'Estado']]
    for cliente in clientes:
        clientes_data.append([
            cliente.nombre[:25],
            cliente.documento,
            cliente.email[:25] if cliente.email else 'N/A',
            cliente.get_estado_display()
        ])
    
    clientes_table = Table(clientes_data, colWidths=[2*inch, 1.2*inch, 2*inch, 1*inch])
    clientes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1cc88a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
    ]))
    
    elements.append(clientes_table)
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_clientes_{datetime.now().strftime("%Y%m%d")}.pdf"'
    response.write(pdf)
    
    return response

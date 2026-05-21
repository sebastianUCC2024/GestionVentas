from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.core.mail import send_mail

from clientes.models import Cliente
from .models import OportunidadVenta, Seguimiento
from .forms import OportunidadVentaForm, SeguimientoForm
from users.decorators import vendedor_required, admin_required


@login_required
def venta_list(request):
    query = request.GET.get('q')
    estado = request.GET.get('estado')

    ventas = OportunidadVenta.objects.select_related('cliente', 'vendedor').all()

    if query:
        ventas = ventas.filter(
            Q(id__icontains=query) |
            Q(titulo__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__documento__icontains=query)
        )

    if estado:
        ventas = ventas.filter(estado=estado)

    return render(request, 'ventas/venta_list.html', {
        'ventas': ventas,
        'query': query,
        'estado': estado,
        'total_ventas': ventas.count(),
        'total_monto': ventas.aggregate(total=Sum('monto'))['total'] or 0,
        'ventas_ganadas': ventas.filter(estado='ganada').count(),
        'ventas_perdidas': ventas.filter(estado='perdida').count(),
    })


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
        'seguimientos': seguimientos
    })


@login_required
@vendedor_required
def venta_create(request):
    if request.method == 'POST':
        form = OportunidadVentaForm(request.POST)

        if form.is_valid():
            venta = form.save(commit=False)

            if not venta.vendedor:
                venta.vendedor = request.user

            venta.save()
            messages.success(request, 'Oportunidad de venta creada correctamente.')
            return redirect('venta_list')
    else:
        form = OportunidadVentaForm(initial={'vendedor': request.user})

    return render(request, 'ventas/venta_form.html', {'form': form})


@login_required
@vendedor_required
def venta_update(request, pk):
    venta = get_object_or_404(OportunidadVenta, pk=pk)

    if request.method == 'POST':
        form = OportunidadVentaForm(request.POST, instance=venta)

        if form.is_valid():
            form.save()
            messages.success(request, 'Oportunidad de venta actualizada correctamente.')
            return redirect('venta_list')
    else:
        form = OportunidadVentaForm(instance=venta)

    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'venta': venta
    })


@login_required
@admin_required
def venta_delete(request, pk):
    venta = get_object_or_404(OportunidadVenta, pk=pk)

    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Oportunidad de venta eliminada correctamente.')
        return redirect('venta_list')

    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})


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
            Q(id__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__documento__icontains=query) |
            Q(oportunidad__titulo__icontains=query) |
            Q(observaciones__icontains=query)
        )

    if tipo:
        seguimientos = seguimientos.filter(tipo_contacto=tipo)

    return render(request, 'ventas/seguimiento_list.html', {
        'seguimientos': seguimientos,
        'query': query,
        'tipo': tipo,
        'total_seguimientos': seguimientos.count(),
        'pendientes': seguimientos.filter(completado=False).count(),
        'completados': seguimientos.filter(completado=True).count(),
    })


@login_required
def seguimiento_detail(request, pk):
    seguimiento = get_object_or_404(
        Seguimiento.objects.select_related('cliente', 'oportunidad', 'usuario'),
        pk=pk
    )

    return render(request, 'ventas/seguimiento_detail.html', {
        'seguimiento': seguimiento
    })


@login_required
@vendedor_required
def seguimiento_create(request):
    if request.method == 'POST':
        form = SeguimientoForm(request.POST)

        if form.is_valid():
            seguimiento = form.save(commit=False)

            if not seguimiento.usuario:
                seguimiento.usuario = request.user

            seguimiento.save()

            if seguimiento.cliente.correo:
                send_mail(
                    subject='Nuevo seguimiento registrado',
                    message=(
                        f'Hola {seguimiento.cliente.nombre},\n\n'
                        f'Se ha registrado un nuevo seguimiento en GestionVentas.\n'
                        f'Oportunidad: {seguimiento.oportunidad.titulo}\n'
                        f'Tipo de contacto: {seguimiento.get_tipo_contacto_display()}\n'
                        f'Próximo contacto: {seguimiento.proximo_contacto or "No definido"}\n\n'
                        f'Observaciones:\n{seguimiento.observaciones}'
                    ),
                    from_email='noreply@gestionventas.com',
                    recipient_list=[seguimiento.cliente.correo],
                    fail_silently=True,
                )

            messages.success(request, 'Seguimiento registrado correctamente.')
            return redirect('seguimiento_list')
    else:
        form = SeguimientoForm(initial={'usuario': request.user})

    return render(request, 'ventas/seguimiento_form.html', {'form': form})


@login_required
@vendedor_required
def seguimiento_update(request, pk):
    seguimiento = get_object_or_404(Seguimiento, pk=pk)

    if request.method == 'POST':
        form = SeguimientoForm(request.POST, instance=seguimiento)

        if form.is_valid():
            form.save()
            messages.success(request, 'Seguimiento actualizado correctamente.')
            return redirect('seguimiento_list')
    else:
        form = SeguimientoForm(instance=seguimiento)

    return render(request, 'ventas/seguimiento_form.html', {
        'form': form,
        'seguimiento': seguimiento
    })


@login_required
@admin_required
def seguimiento_delete(request, pk):
    seguimiento = get_object_or_404(Seguimiento, pk=pk)

    if request.method == 'POST':
        seguimiento.delete()
        messages.success(request, 'Seguimiento eliminado correctamente.')
        return redirect('seguimiento_list')

    return render(request, 'ventas/seguimiento_confirm_delete.html', {
        'seguimiento': seguimiento
    })


@login_required
def ventas_dashboard(request):
    hoy = timezone.now().date()
    limite = hoy + timedelta(days=7)

    total_clientes = Cliente.objects.count()
    total_ventas = OportunidadVenta.objects.count()

    clientes_activos = Cliente.objects.filter(estado='activo').count()
    clientes_inactivos = Cliente.objects.filter(estado='inactivo').count()

    total_ingresos = OportunidadVenta.objects.filter(
        estado='ganada'
    ).aggregate(total=Sum('monto'))['total'] or 0

    ventas_por_estado = (
        OportunidadVenta.objects
        .values('estado')
        .annotate(total=Count('id'))
        .order_by('estado')
    )

    ventas_por_mes = (
        OportunidadVenta.objects
        .annotate(mes=TruncMonth('fecha_creacion'))
        .values('mes')
        .annotate(total=Count('id'), ingresos=Sum('monto'))
        .order_by('mes')
    )

    ventas_por_vendedor = (
        OportunidadVenta.objects
        .values('vendedor__username')
        .annotate(total=Count('id'), ingresos=Sum('monto'))
        .order_by('-total')[:5]
    )

    recordatorios_proximos = (
        Seguimiento.objects
        .filter(completado=False, proximo_contacto__range=[hoy, limite])
        .select_related('cliente', 'oportunidad', 'usuario')
        .order_by('proximo_contacto')[:6]
    )

    recordatorios_vencidos = (
        Seguimiento.objects
        .filter(completado=False, proximo_contacto__lt=hoy)
        .select_related('cliente', 'oportunidad', 'usuario')
        .order_by('proximo_contacto')[:6]
    )

    ventas_recientes = (
        OportunidadVenta.objects
        .select_related('cliente', 'vendedor')
        .order_by('-fecha_creacion')[:5]
    )

    clientes_por_estado = [
        {'estado': 'Activos', 'total': clientes_activos},
        {'estado': 'Inactivos', 'total': clientes_inactivos},
    ]

    return render(request, 'ventas/ventas_dashboard.html', {
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
        'total_ingresos': total_ingresos,
        'ventas_ganadas': OportunidadVenta.objects.filter(estado='ganada').count(),
        'ventas_perdidas': OportunidadVenta.objects.filter(estado='perdida').count(),
        'seguimientos': Seguimiento.objects.count(),
        'ventas_por_estado': ventas_por_estado,
        'ventas_por_mes': ventas_por_mes,
        'ventas_por_vendedor': ventas_por_vendedor,
        'recordatorios_proximos': recordatorios_proximos,
        'recordatorios_vencidos': recordatorios_vencidos,
        'ventas_recientes': ventas_recientes,
        'clientes_por_estado': clientes_por_estado,
    })
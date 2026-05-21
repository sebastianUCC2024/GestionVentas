from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count

from clientes.models import Cliente
from .models import OportunidadVenta, Seguimiento
from .forms import OportunidadVentaForm, SeguimientoForm
from users.decorators import vendedor_required, admin_required


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

    return render(request, 'ventas/venta_list.html', {
        'ventas': ventas,
        'query': query,
        'estado': estado,
        'total_ventas': total_ventas,
        'total_monto': total_monto,
        'ventas_ganadas': ventas_ganadas,
        'ventas_perdidas': ventas_perdidas,
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
        'seguimientos': seguimientos,
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

    return render(request, 'ventas/venta_form.html', {
        'form': form
    })


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
        'venta': venta,
    })


@login_required
@admin_required
def venta_delete(request, pk):
    venta = get_object_or_404(OportunidadVenta, pk=pk)

    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Oportunidad de venta eliminada correctamente.')
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

    return render(request, 'ventas/seguimiento_list.html', {
        'seguimientos': seguimientos,
        'query': query,
        'tipo': tipo,
        'total_seguimientos': total_seguimientos,
        'pendientes': pendientes,
        'completados': completados,
    })


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
@vendedor_required
def seguimiento_create(request):
    if request.method == 'POST':
        form = SeguimientoForm(request.POST)

        if form.is_valid():
            seguimiento = form.save(commit=False)

            if not seguimiento.usuario:
                seguimiento.usuario = request.user

            seguimiento.save()
            messages.success(request, 'Seguimiento registrado correctamente.')
            return redirect('seguimiento_list')
    else:
        form = SeguimientoForm(initial={'usuario': request.user})

    return render(request, 'ventas/seguimiento_form.html', {
        'form': form
    })


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
        'seguimiento': seguimiento,
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

    return render(request, 'ventas/ventas_dashboard.html', {
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
    })
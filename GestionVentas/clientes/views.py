from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm


@login_required
def cliente_list(request):
    query = request.GET.get('q')
    estado = request.GET.get('estado')

    clientes = Cliente.objects.all().order_by('-fecha_registro')

    if query:
        clientes = clientes.filter(nombre__icontains=query) | clientes.filter(documento__icontains=query) | clientes.filter(correo__icontains=query)

    if estado:
        clientes = clientes.filter(estado=estado)

    return render(request, 'clientes/cliente_list.html', {
        'clientes': clientes,
        'query': query,
        'estado': estado
    })


@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/cliente_detail.html', {'cliente': cliente})


@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()

    return render(request, 'clientes/cliente_form.html', {'form': form})


@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/cliente_form.html', {'form': form})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('cliente_list')

    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})
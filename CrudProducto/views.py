
# Create your views here.
# CrudProducto/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Orden, Cliente, Repartidor
from .forms import ProductoForm, OrdenForm, ClienteForm, RepartidorForm, OrdenPaso1Form, RepartidorSeleccionForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

# ---------------- PRODUCTOS ------------------
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto.html', {
        'productos': productos,
        'title': 'Lista de Productos',
        'vista': 'lista'
    })

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto.html', {
        'form': form,
        'title': 'Crear Producto',
        'vista': 'form'
    })

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto.html', {
        'form': form,
        'title': 'Actualizar Producto',
        'vista': 'form'
    })

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:listar_productos')
    return render(request, 'producto.html', {
        'producto': producto,
        'title': 'Eliminar Producto',
        'vista': 'delete'
    })

# ---------------- ORDENES EN TRES PASOS ------------------
def listar_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'orden.html', {
        'ordenes': ordenes,
        'title': 'Lista de Órdenes',
        'vista': 'lista'
    })

def crear_orden_paso1(request):
    if request.method == 'POST':
        form = OrdenPaso1Form(request.POST)
        if form.is_valid():
            request.session['producto_id'] = form.cleaned_data['producto'].id
            request.session['cantidad'] = form.cleaned_data['cantidad']
            return redirect('productos:crear_orden_paso2')
    else:
        form = OrdenPaso1Form()
    return render(request, 'orden_paso1.html', {'form': form, 'title': 'Paso 1: Selección de Producto'})

def crear_orden_paso2(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            request.session['cliente_id'] = cliente.id
            return redirect('productos:crear_orden_paso3')
    else:
        form = ClienteForm()
    return render(request, 'orden_paso2.html', {'form': form, 'title': 'Paso 2: Datos del Cliente'})

def crear_orden_paso3(request):
    if request.method == 'POST':
        form = RepartidorSeleccionForm(request.POST)
        if form.is_valid():
            repartidor = form.cleaned_data['repartidor']
            producto = get_object_or_404(Producto, pk=request.session['producto_id'])
            cantidad = request.session['cantidad']
            cliente = get_object_or_404(Cliente, pk=request.session['cliente_id'])
            orden = Orden(producto=producto, cantidad=cantidad)
            orden.save()
            producto.stock -= int(cantidad)
            producto.save()
            repartidor.disponible = 'No'
            repartidor.save()
            request.session.flush()
            return redirect('home')
    else:
        form = RepartidorSeleccionForm()
    return render(request, 'orden_paso3.html', {'form': form, 'title': 'Paso 3: Selección de Repartidor'})

def eliminar_orden(request, id):
    orden = get_object_or_404(Orden, pk=id)
    if request.method == 'POST':
        orden.producto.stock += orden.cantidad
        orden.producto.save()
        orden.delete()
        return redirect('productos:listar_ordenes')
    return render(request, 'orden.html', {
        'orden': orden,
        'title': 'Eliminar Orden',
        'vista': 'delete'
    })

# ---------------- CLIENTES ------------------
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente.html', {
        'clientes': clientes,
        'title': 'Lista de Clientes',
        'vista': 'lista'
    })

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'cliente.html', {
        'form': form,
        'title': 'Crear Cliente',
        'vista': 'form'
    })

def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente.html', {
        'form': form,
        'title': 'Editar Cliente',
        'vista': 'form'
    })

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('productos:listar_clientes')
    return render(request, 'cliente.html', {
        'cliente': cliente,
        'title': 'Eliminar Cliente',
        'vista': 'delete'
    })

# ---------------- REPARTIDORES ------------------
def listar_repartidores(request):
    repartidores = Repartidor.objects.all().order_by('apellidos', 'nombre')  # Orden alfabético
    return render(request, 'repartidor.html', {
        'repartidores': repartidores,
        'title': 'Lista de Repartidores',
        'vista': 'lista'
    })


def crear_repartidor(request):
    if request.method == 'POST':
        form = RepartidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_repartidores')
    else:
        form = RepartidorForm(initial={'disponible': 'Si'})  # Valor por defecto

    return render(request, 'repartidor.html', {
        'form': form,
        'title': 'Crear Repartidor',
        'vista': 'form'
    })


def actualizar_repartidor(request, id):
    repartidor = get_object_or_404(Repartidor, pk=id)
    if request.method == 'POST':
        form = RepartidorForm(request.POST, instance=repartidor)
        if form.is_valid():
            form.save()
            return redirect('productos:listar_repartidores')
    else:
        form = RepartidorForm(instance=repartidor)

    return render(request, 'repartidor.html', {
        'form': form,
        'title': f'Editar Repartidor: {repartidor.nombre}',
        'vista': 'form'
    })


def eliminar_repartidor(request, id):
    repartidor = get_object_or_404(Repartidor, pk=id)
    if request.method == 'POST':
        repartidor.delete()
        return redirect('productos:listar_repartidores')

    return render(request, 'repartidor.html', {
        'repartidor': repartidor,
        'title': f'Eliminar Repartidor: {repartidor.nombre}',
        'vista': 'delete'
    })


# ---------------- BACKUP ------------------
# ---------------- BACKUP ------------------

def descargar_backup(request):
    buffer = io.StringIO()
    management.call_command('dumpdata', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response

from django.core import management
import io
from django.http import HttpResponse

def descargar_backup(request):
    buffer = io.StringIO()
    management.call_command('dumpdata', stdout=buffer)
    response = HttpResponse(buffer.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response

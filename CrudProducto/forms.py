# CrudProducto/forms.py
from django import forms
from .models import Producto, Orden, Cliente, Repartidor

# Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Orden
class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['producto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")

        if producto and cantidad:
            if cantidad > producto.stock:
                self.add_error('cantidad', f"Solo hay {producto.stock} unidades disponibles.")

# Paso 1 - Selección de producto y cantidad
class OrdenPaso1Form(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(stock__gt=0))
    cantidad = forms.IntegerField(min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get("producto")
        cantidad = cleaned_data.get("cantidad")

        if producto and cantidad:
            if cantidad > producto.stock:
                self.add_error('cantidad', f"Solo hay {producto.stock} unidades disponibles.")

# Paso 3 - Selección de repartidor disponible
class RepartidorSeleccionForm(forms.Form):
    repartidor = forms.ModelChoiceField(queryset=Repartidor.objects.filter(disponible='Si'))

# Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'cedula', 'telefono', 'correo', 'cliente_frecuente']

# Repartidor
class RepartidorForm(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ['nombre', 'apellidos', 'cedula', 'telefono', 'correo', 'disponible']
        widgets = {
            'disponible': forms.Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 200px;'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'disponible': 'Estado de disponibilidad'
        }
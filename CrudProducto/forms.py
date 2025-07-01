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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.replace(" ", "").isalpha():
            raise forms.ValidationError("Los apellidos solo deben contener letras.")
        return apellidos

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        if len(cedula) < 8 or len(cedula) > 10:
            raise forms.ValidationError("La cédula debe tener entre 8 y 10 dígitos.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if len(telefono) < 7 or len(telefono) > 10:
            raise forms.ValidationError("El teléfono debe tener entre 7 y 10 dígitos.")
        return telefono

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

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.replace(" ", "").isalpha():
            raise forms.ValidationError("Los apellidos solo deben contener letras.")
        return apellidos

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        if len(cedula) < 8 or len(cedula) > 10:
            raise forms.ValidationError("La cédula debe tener entre 8 y 10 dígitos.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if len(telefono) < 7 or len(telefono) > 10:
            raise forms.ValidationError("El teléfono debe tener entre 7 y 10 dígitos.")
        return telefono

    def clean(self):
        cleaned_data = super().clean()
        cedula = cleaned_data.get('cedula')
        telefono = cleaned_data.get('telefono')

        # Obtener instancia si existe (en edición)
        instance = self.instance

        if cedula:
            # Si estamos creando o la cédula cambió
            qs = Repartidor.objects.filter(cedula=cedula)
            if instance.pk:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                self.add_error('cedula', "Repartidor ya registrado con esta cédula.")

        if telefono:
            qs = Repartidor.objects.filter(telefono=telefono)
            if instance.pk:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                self.add_error('telefono', "Ya existe un repartidor con este número de teléfono.")

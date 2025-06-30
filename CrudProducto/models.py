
#aqui colocamos nuestra primera clase para nuestro producto
from django.db import models
#clase producto


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} - ${self.precio} (Stock: {self.stock})"
#clase orden
class Orden(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, limit_choices_to={'stock__gt': 0})  # Solo productos con stock > 0
    cantidad = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.producto.nombre}"


#clase persona para cliente y para repartidor
# Clase base abstracta
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    class Meta:
        abstract = True  # No se creará tabla en la BD

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# Clase Cliente que hereda de Persona
class Cliente(Persona):
    OPCIONES = [
        ('Si', 'Sí'),
        ('No', 'No'),
    ]
    cliente_frecuente = models.CharField(max_length=2, choices=OPCIONES)

    def __str__(self):
        return f"{super().__str__()} - Frecuente: {self.cliente_frecuente}"


#repartidor
# models.py

class Repartidor(Persona):
    OPCIONES = [
        ('Si', 'Sí'),
        ('No', 'No'),
    ]
    disponible = models.CharField(
        max_length=2,
        choices=OPCIONES,
        default='Si',  # Establece un valor por defecto
        verbose_name="Disponibilidad"
    )

    def __str__(self):
        return f"{super().__str__()} - Disponible: {self.get_disponible_display()}"
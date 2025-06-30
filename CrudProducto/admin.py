from django.contrib import admin
from .models import Producto
from .models import Orden
from .models import Cliente
from .models import Repartidor

admin.site.register(Repartidor)
admin.site.register(Cliente)
admin.site.register(Producto)
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'fecha_creacion')
    list_filter = ('producto', 'fecha_creacion')
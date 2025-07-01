# CrudProducto/urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Productos
    path('', views.listar_productos, name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Órdenes
    path('ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('ordenes/eliminar/<int:id>/', views.eliminar_orden, name='eliminar_orden'),
    path('ordenes/crear/', views.crear_orden_paso1, name='crear_orden'),
    path('ordenes/paso2/', views.crear_orden_paso2, name='crear_orden_paso2'),
    path('ordenes/paso3/', views.crear_orden_paso3, name='crear_orden_paso3'),

    # Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Repartidores
    path('repartidores/', views.listar_repartidores, name='listar_repartidores'),
    path('repartidores/crear/', views.crear_repartidor, name='crear_repartidor'),
    path('repartidores/editar/<int:id>/', views.actualizar_repartidor, name='actualizar_repartidor'),
    path('repartidores/eliminar/<int:id>/', views.eliminar_repartidor, name='eliminar_repartidor'),

    #pasos
    path('ordenes/paso1/', views.crear_orden_paso1, name='orden_paso1'),
    path('ordenes/paso2/', views.crear_orden_paso2, name='orden_paso2'),
    path('ordenes/paso3/', views.crear_orden_paso3, name='orden_paso3'),
    #backup
    path('backup/', views.descargar_backup, name='descargar_backup'),

]

# Generated by Django 5.2.3 on 2025-06-29 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CrudProducto', '0003_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repartidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
                ('disponible', models.CharField(choices=[('Si', 'Sí'), ('No', 'No')], max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

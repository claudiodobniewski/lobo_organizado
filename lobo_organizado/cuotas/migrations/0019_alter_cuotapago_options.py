# Generated by Django 3.2 on 2021-05-03 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0018_alter_cuotasocialfamilia_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuotapago',
            options={'permissions': (('pago_cuota_crear', 'Agregar nuevas cuotas de un plan a familia'), ('pago_cuota_editar', 'Editar cuotas de un plan a familia'), ('pago_cuota_borrar', 'Eliminar cuotas de un plan a familia'), ('pago_cuota_ver', 'Ver detalle de cuotas del plan a familia'))},
        ),
    ]

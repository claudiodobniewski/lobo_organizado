# Generated by Django 3.2 on 2021-05-14 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0020_alter_cuotasocialfamilia_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuotapago',
            options={'permissions': (('pago_cuota_crear', 'Agregar nuevos pagos de un plan a familia'), ('pago_cuota_editar', 'Editar pagos a un plan de la familia'), ('pago_cuota_borrar', 'Eliminar pagos de un plan a familia'), ('pago_cuota_ver', 'Ver detalle de pagos del plan a familia'))},
        ),
    ]
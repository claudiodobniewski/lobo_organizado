# Generated by Django 3.1.7 on 2021-03-28 19:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('socios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanDePago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm_id', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=300)),
                ('creado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 626101, tzinfo=utc), verbose_name='creado')),
                ('actualizado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 626150, tzinfo=utc), verbose_name='actualizado')),
                ('cantidad_cuotas', models.IntegerField(verbose_name='cantidad_cuotas')),
                ('vto_primera_cuota', models.DateField(verbose_name='vto_primera_cuota')),
                ('importe_cuota', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CuotaSocialFamilia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vencimiento', models.DateField(verbose_name='vencimiento')),
                ('importe_cuota', models.FloatField()),
                ('creado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 626818, tzinfo=utc), verbose_name='creado')),
                ('actualizado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 626847, tzinfo=utc), verbose_name='actualizado')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socios.familia')),
                ('plan_de_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuotas.plandepago')),
            ],
        ),
        migrations.CreateModel(
            name='CuotaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cobrado', models.DateField(verbose_name='vencimiento')),
                ('creado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 627513, tzinfo=utc), verbose_name='creado')),
                ('actualizado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 627542, tzinfo=utc), verbose_name='actualizado')),
                ('aplica_cuota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuotas.cuotasocialfamilia')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socios.familia')),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-03-28 19:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('familia_crm_id', models.CharField(max_length=50)),
                ('creado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 589222, tzinfo=utc), verbose_name='creado')),
                ('actualizado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 589257, tzinfo=utc), verbose_name='actualizado')),
            ],
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('dni', models.CharField(max_length=15)),
                ('fecha_nacimiento', models.DateField(verbose_name='fecha_nacimiento')),
                ('creado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 614919, tzinfo=utc), verbose_name='creado')),
                ('actualizado', models.DateTimeField(default=datetime.datetime(2021, 3, 28, 19, 50, 31, 614944, tzinfo=utc), verbose_name='actualizado')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socios.familia')),
            ],
        ),
    ]

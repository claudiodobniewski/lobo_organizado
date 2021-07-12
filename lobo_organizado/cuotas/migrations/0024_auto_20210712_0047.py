# Generated by Django 3.2.5 on 2021-07-12 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0023_auto_20210711_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotapago',
            name='forma_de_pago',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cuotas.cuotamediodepago'),
        ),
        migrations.AlterField(
            model_name='cuotamediodepago',
            name='medio_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
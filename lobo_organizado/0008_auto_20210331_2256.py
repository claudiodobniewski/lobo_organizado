# Generated by Django 3.1.7 on 2021-03-31 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0007_auto_20210331_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='observaciones',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='socios.observaciones'),
        ),
    ]
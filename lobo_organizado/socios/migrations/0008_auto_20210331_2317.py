# Generated by Django 3.1.7 on 2021-03-31 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0007_auto_20210331_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familia',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='observaciones',
            name='familia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socios.familia'),
        ),
    ]

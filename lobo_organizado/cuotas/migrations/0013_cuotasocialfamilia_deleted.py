# Generated by Django 3.1.7 on 2021-04-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0012_plandepago_eliminado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotasocialfamilia',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
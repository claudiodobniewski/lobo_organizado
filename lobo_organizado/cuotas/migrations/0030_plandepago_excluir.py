# Generated by Django 3.2 on 2023-04-10 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0029_alter_cuotapago_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='plandepago',
            name='excluir',
            field=models.BooleanField(default=False),
        ),
    ]
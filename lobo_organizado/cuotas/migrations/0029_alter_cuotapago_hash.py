# Generated by Django 3.2 on 2022-03-28 00:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0028_cuotapago_remove_hash_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotapago',
            name='hash',
            field=models.CharField(default=uuid.uuid4, max_length=40),
        ),
    ]
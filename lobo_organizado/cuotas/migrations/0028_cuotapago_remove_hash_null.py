# Generated by Django 3.2 on 2022-03-14 03:42

import cuotas.models
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('cuotas', '0027_cuotapago_populate_hash_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuotapago',
            name='hash',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]


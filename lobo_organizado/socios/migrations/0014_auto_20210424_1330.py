# Generated by Django 3.1.7 on 2021-04-24 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0013_auto_20210419_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='familia_crm_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
# Generated by Django 4.2 on 2023-10-27 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_meb_delete_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meb',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]

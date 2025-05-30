# Generated by Django 3.2.25 on 2025-02-03 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20250203_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('for_rent', 'Available for Rent'), ('for_sale', 'Available for Purchase'), ('rented_out', 'Rented Out'), ('sold', 'Sold')], default='for_sale', max_length=50),
        ),
    ]

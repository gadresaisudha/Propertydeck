# Generated by Django 3.2.25 on 2025-02-03 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_property_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.property'),
        ),
    ]

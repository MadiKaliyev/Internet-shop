# Generated by Django 4.2.9 on 2024-11-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tovari', '0002_alter_products_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

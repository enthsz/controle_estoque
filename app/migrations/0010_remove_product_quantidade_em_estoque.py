# Generated by Django 5.0.6 on 2024-06-15 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_product_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantidade_em_estoque',
        ),
    ]
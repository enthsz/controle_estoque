# Generated by Django 5.0.6 on 2024-06-18 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_product_options_rename_produto_sale_produto_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='quantidade',
            new_name='vendidos',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]

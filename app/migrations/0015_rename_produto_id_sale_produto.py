# Generated by Django 5.0.6 on 2024-06-16 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_product_quantidade_em_estoque'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='produto_id',
            new_name='produto',
        ),
    ]

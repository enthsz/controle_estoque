# Generated by Django 5.0.6 on 2024-06-14 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_food_product_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='nome',
        ),
    ]

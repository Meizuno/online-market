# Generated by Django 4.1.4 on 2023-02-03 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_alter_cart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='item',
            new_name='crop',
        ),
    ]
# Generated by Django 4.1.4 on 2023-02-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_rename_item_cart_crop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='amount',
            field=models.IntegerField(max_length=20, verbose_name='Amount'),
        ),
    ]

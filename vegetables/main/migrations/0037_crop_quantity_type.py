# Generated by Django 4.1.4 on 2023-02-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_crop_editing'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='quantity_type',
            field=models.CharField(default=0, max_length=20, verbose_name='Type of quantity'),
        ),
    ]

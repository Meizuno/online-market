# Generated by Django 4.1.4 on 2023-01-06 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_crop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='image',
            field=models.ImageField(blank=True, default='no_image.png', null=True, upload_to='crop_images', verbose_name='Foto'),
        ),
    ]
# Generated by Django 4.1.4 on 2023-01-06 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Foto'),
        ),
    ]

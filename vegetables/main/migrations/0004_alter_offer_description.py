# Generated by Django 4.1.4 on 2022-12-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_crop_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(default=None, verbose_name='Description'),
        ),
    ]

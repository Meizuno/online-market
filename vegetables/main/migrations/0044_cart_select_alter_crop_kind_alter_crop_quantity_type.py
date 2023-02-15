# Generated by Django 4.1.4 on 2023-02-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_alter_crop_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='select',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='kind',
            field=models.CharField(default='vegetable', max_length=20, verbose_name='Kind'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='quantity_type',
            field=models.CharField(default='kg', max_length=20, verbose_name='Type of quantity'),
        ),
    ]

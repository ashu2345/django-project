# Generated by Django 2.1.8 on 2019-04-24 12:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190424_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

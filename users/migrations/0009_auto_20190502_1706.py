# Generated by Django 2.2 on 2019-05-02 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190425_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('descr', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartorders',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='cartorders',
            name='order_time',
        ),
        migrations.RemoveField(
            model_name='cartorders',
            name='price',
        ),
        migrations.RemoveField(
            model_name='cartorders',
            name='type_of_food',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='order_time',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='price',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='type_of_food',
        ),
        migrations.AddField(
            model_name='cartorders',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='users.Item'),
        ),
        migrations.AddField(
            model_name='orders',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conf_item', to='users.Item'),
        ),
    ]
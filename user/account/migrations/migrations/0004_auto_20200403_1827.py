# Generated by Django 2.2.7 on 2020-04-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_order_prices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='slug',
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

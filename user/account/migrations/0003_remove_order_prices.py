# Generated by Django 2.2.7 on 2020-04-03 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_book_perprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Prices',
        ),
    ]
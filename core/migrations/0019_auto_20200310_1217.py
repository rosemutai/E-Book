# Generated by Django 2.2 on 2020-03-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.IntegerField(),
        ),
    ]

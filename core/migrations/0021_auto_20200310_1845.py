# Generated by Django 2.2 on 2020-03-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]

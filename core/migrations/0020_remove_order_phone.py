# Generated by Django 2.2 on 2020-03-10 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200310_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
    ]

# Generated by Django 2.2 on 2020-03-09 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200309_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['id']},
        ),
    ]

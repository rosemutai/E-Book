# Generated by Django 2.2 on 2020-03-09 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_shopapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ShopApplication')),
            ],
        ),
    ]
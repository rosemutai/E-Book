# Generated by Django 2.2 on 2020-03-06 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200306_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MerchantRequestID', models.CharField(max_length=250, null=True)),
                ('CheckoutRequestID', models.CharField(max_length=250, null=True)),
                ('ResultCode', models.IntegerField(null=True)),
                ('ResultDesc', models.CharField(max_length=250, null=True)),
                ('Amount', models.CharField(max_length=250, null=True)),
                ('MpesaReceiptNumber', models.CharField(max_length=250, null=True)),
                ('Balance', models.CharField(max_length=250, null=True)),
                ('TransactionDate', models.CharField(max_length=250, null=True)),
                ('PhoneNumber', models.CharField(max_length=250, null=True)),
            ],
            options={
                'ordering': ['TransactionDate'],
            },
        ),
    ]
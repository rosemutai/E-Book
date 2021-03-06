# Generated by Django 2.2 on 2020-03-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200308_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('SP', 'Sports'), ('N', 'Novels'), ('A', 'Art')], max_length=2),
        ),
        migrations.AlterField(
            model_name='languages',
            name='category',
            field=models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('SP', 'Sports'), ('N', 'Novels'), ('A', 'Art')], max_length=2),
        ),
        migrations.AlterField(
            model_name='novels',
            name='category',
            field=models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('SP', 'Sports'), ('N', 'Novels'), ('A', 'Art')], max_length=2),
        ),
        migrations.AlterField(
            model_name='sciences',
            name='category',
            field=models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('SP', 'Sports'), ('N', 'Novels'), ('A', 'Art')], max_length=2),
        ),
        migrations.AlterField(
            model_name='stationery',
            name='category',
            field=models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('SP', 'Sports'), ('N', 'Novels'), ('A', 'Art')], max_length=2),
        ),
    ]

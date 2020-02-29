# Generated by Django 2.2 on 2020-02-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sciences'),
    ]

    operations = [
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('P', 'Pens'), ('TB', 'Text Books'), ('EB', 'Exercise Books'), ('ST', 'Story Books'), ('N', 'Novels')], max_length=2)),
                ('label', models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]

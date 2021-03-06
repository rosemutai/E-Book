# Generated by Django 2.2 on 2020-03-07 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('isbn', models.CharField(max_length=13, verbose_name='ISBN')),
                ('total_copies', models.IntegerField()),
                ('available_copies', models.IntegerField()),
                ('pic', models.ImageField(blank=True, null=True, upload_to='book_image')),
                ('genre', models.ManyToManyField(to='library.Genre')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.Language')),
            ],
        ),
    ]

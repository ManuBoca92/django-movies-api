# Generated by Django 2.2.12 on 2020-05-07 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movie',
            new_name='movie_detail',
        ),
    ]

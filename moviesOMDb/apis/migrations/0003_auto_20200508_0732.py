# Generated by Django 2.2.12 on 2020-05-08 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_auto_20200507_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='movie_comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='movie',
            new_name='movie_id',
        ),
    ]

# Generated by Django 2.0 on 2017-12-20 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contents',
            new_name='Posts',
        ),
    ]
# Generated by Django 2.0 on 2018-01-17 10:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_author_user_pwd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='reg_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 17, 10, 20, 17, 551291, tzinfo=utc), verbose_name='registered'),
        ),
        migrations.AlterField(
            model_name='author',
            name='user_pwd',
            field=models.CharField(default='', max_length=100),
        ),
    ]
# Generated by Django 2.0 on 2017-12-28 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20171220_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='user_pwd',
            field=models.CharField(default=1234567, max_length=100),
            preserve_default=False,
        ),
    ]

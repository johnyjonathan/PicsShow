# Generated by Django 3.1.2 on 2021-03-21 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0003_auto_20210321_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimage',
            name='date',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='username',
        ),
    ]
# Generated by Django 3.1.2 on 2021-03-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0005_userimage_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

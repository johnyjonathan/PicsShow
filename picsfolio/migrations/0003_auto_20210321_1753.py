# Generated by Django 3.1.2 on 2021-03-21 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0002_auto_20210321_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='image',
            field=models.ImageField(upload_to='piscfolio/images'),
        ),
    ]

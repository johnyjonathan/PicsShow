# Generated by Django 3.1.2 on 2021-03-21 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0012_auto_20210321_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='piscfolio/images'),
        ),
    ]

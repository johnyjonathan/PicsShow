# Generated by Django 3.1.7 on 2021-04-03 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0016_auto_20210402_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercatalog',
            name='imagesList',
            field=models.TextField(null=True),
        ),
    ]

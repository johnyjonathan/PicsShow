# Generated by Django 3.1.7 on 2021-04-04 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picsfolio', '0018_auto_20210403_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimage',
            name='catalog',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='picsfolio.usercatalog'),
        ),
    ]

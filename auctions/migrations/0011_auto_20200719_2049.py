# Generated by Django 3.0.8 on 2020-07-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200719_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(default='Not Specified', max_length=64, unique=True),
        ),
    ]

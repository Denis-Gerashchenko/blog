# Generated by Django 2.1.9 on 2019-06-24 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20190623_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='viewcount',
            field=models.IntegerField(default=0),
        ),
    ]

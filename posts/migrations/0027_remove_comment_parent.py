# Generated by Django 2.1.10 on 2019-07-08 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
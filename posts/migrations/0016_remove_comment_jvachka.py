# Generated by Django 2.1.9 on 2019-06-29 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_comment_jvachka'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='jvachka',
        ),
    ]

# Generated by Django 2.2.6 on 2021-04-08 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20210408_0627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Follow'},
        ),
    ]

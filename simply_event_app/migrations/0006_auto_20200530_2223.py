# Generated by Django 3.0.6 on 2020-05-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simply_event_app', '0005_auto_20200530_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='delay',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Delay in minutes'),
        ),
    ]

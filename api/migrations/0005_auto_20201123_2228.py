# Generated by Django 3.0.5 on 2020-11-23 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201117_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='code',
            field=models.IntegerField(default=7757, verbose_name='Confirmation code'),
        ),
    ]

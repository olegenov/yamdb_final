# Generated by Django 3.0.5 on 2020-11-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201123_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='code',
            field=models.IntegerField(default=7635, verbose_name='Confirmation code'),
        ),
    ]
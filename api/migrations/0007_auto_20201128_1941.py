# Generated by Django 3.0.5 on 2020-11-28 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201123_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='code',
            field=models.IntegerField(default=3362, verbose_name='Confirmation code'),
        ),
    ]
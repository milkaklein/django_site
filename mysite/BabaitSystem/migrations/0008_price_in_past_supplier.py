# Generated by Django 2.2 on 2019-06-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BabaitSystem', '0007_auto_20190613_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='price_in_past',
            name='supplier',
            field=models.CharField(default='', max_length=20),
        ),
    ]

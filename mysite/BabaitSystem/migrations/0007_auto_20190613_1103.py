# Generated by Django 2.2 on 2019-06-13 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BabaitSystem', '0006_auto_20190613_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbysupplier',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='price_in_past',
            name='date',
            field=models.DateField(),
        ),
    ]
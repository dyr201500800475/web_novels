# Generated by Django 2.0 on 2019-04-09 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0003_auto_20190409_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novelinfo',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]

# Generated by Django 2.0 on 2019-04-09 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0004_auto_20190409_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novelinfo',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.Novel'),
        ),
    ]

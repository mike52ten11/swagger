# Generated by Django 4.2.6 on 2024-10-24 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ami", "0004_device_registered"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="device",
            unique_together={("deviceuuid", "name")},
        ),
    ]
# Generated by Django 4.2.6 on 2024-10-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ami", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="createtime",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

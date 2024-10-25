# Generated by Django 4.2.6 on 2024-10-25 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ami", "0005_alter_device_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElectricNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("electricnumber", models.CharField(max_length=11)),
                ("name", models.CharField(default="", max_length=10)),
                ("createtime", models.DateTimeField(auto_now_add=True)),
                ("registered", models.BooleanField(default=True)),
            ],
            options={
                "unique_together": {("electricnumber", "name")},
            },
        ),
    ]

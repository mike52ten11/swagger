# Generated by Django 4.2.6 on 2024-10-25 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ami", "0007_alter_electricnumber_unique_together_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElectricNumber_Device_Band",
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
                ("createtime", models.DateTimeField(auto_now_add=True)),
                ("registered", models.BooleanField()),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="electric_bands",
                        to="ami.device",
                    ),
                ),
                (
                    "electric",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_bands",
                        to="ami.electricnumber",
                    ),
                ),
            ],
            options={
                "unique_together": {("electric", "device")},
            },
        ),
    ]

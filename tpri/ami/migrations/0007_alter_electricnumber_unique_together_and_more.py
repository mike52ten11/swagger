# Generated by Django 4.2.6 on 2024-10-25 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ami", "0006_electricnumber"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="electricnumber",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="electricnumber",
            name="electricnumber",
            field=models.CharField(max_length=11, unique=True),
        ),
    ]

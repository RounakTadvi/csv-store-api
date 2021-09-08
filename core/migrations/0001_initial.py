# Generated by Django 3.2.5 on 2021-07-29 13:58

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Csv",
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
                ("file_name", models.FileField(upload_to=core.models.csv_file_path)),
                ("uploaded", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
# Generated by Django 3.2.14 on 2022-08-31 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0032_region_bounding_box"),
    ]

    operations = [
        migrations.AlterField(
            model_name="languagetreenode",
            name="visible",
            field=models.BooleanField(
                default=True,
                help_text="Defines whether the language is displayed to the users of the app",
                verbose_name="visible",
            ),
        ),
    ]

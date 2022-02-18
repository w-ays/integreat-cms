# Generated by Django 3.2.12 on 2022-02-18 00:35

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Migration file to add a custom prefix for regions in case the administrative division is not sufficient
    """

    dependencies = [
        ("cms", "0005_grant_imprint_deletion_permission"),
    ]

    operations = [
        migrations.AddField(
            model_name="region",
            name="custom_prefix",
            field=models.CharField(
                blank=True,
                help_text="Enter parts of the name that should not affect sorting. Use this field only if the prefix is not an available choice in the list of administrative divisions above.",
                max_length=48,
                verbose_name="custom prefix",
            ),
        ),
    ]

# Generated by Django 3.2.16 on 2022-12-14 00:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add a migration to rename the author and editor roles for more consistency
    """

    dependencies = [
        ("cms", "0067_add_automatic_translation_field"),
    ]

    operations = [
        migrations.RenameField(
            model_name="page",
            old_name="editors",
            new_name="authors",
        ),
        migrations.AlterField(
            model_name="page",
            name="authors",
            field=models.ManyToManyField(
                blank=True,
                help_text="A list of users who have the permission to edit this specific page. Only has effect if these users do not have the permission to edit pages anyway.",
                related_name="editable_pages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="authors",
            ),
        ),
        migrations.RenameField(
            model_name="page",
            old_name="publishers",
            new_name="editors",
        ),
        migrations.AlterField(
            model_name="page",
            name="editors",
            field=models.ManyToManyField(
                blank=True,
                help_text="A list of users who have the permission to publish this specific page. Only has effect if these users do not have the permission to publish pages anyway.",
                related_name="publishable_pages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="editors",
            ),
        ),
    ]

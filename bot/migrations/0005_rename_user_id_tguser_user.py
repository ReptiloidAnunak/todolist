# Generated by Django 4.2.4 on 2023-08-16 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0004_tguser_verification_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tguser",
            old_name="user_id",
            new_name="user",
        ),
    ]

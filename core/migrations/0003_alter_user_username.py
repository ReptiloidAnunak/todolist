# Generated by Django 4.2.2 on 2023-07-17 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_user_birthdate_alter_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(unique=True, verbose_name=100),
        ),
    ]
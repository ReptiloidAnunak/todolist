# Generated by Django 4.2.2 on 2023-08-08 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0002_alter_tguser_tg_user_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="tguser",
            name="first_name",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="tguser",
            name="last_name",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="tguser",
            name="username",
            field=models.CharField(max_length=150, null=True),
        ),
    ]

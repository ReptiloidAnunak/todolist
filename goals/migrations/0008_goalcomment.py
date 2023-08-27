# Generated by Django 4.2.2 on 2023-07-30 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goals", "0007_alter_goal_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoalComment",
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
                ("created", models.DateTimeField(verbose_name="Дата создания")),
                (
                    "updated",
                    models.DateTimeField(verbose_name="Дата последнего обновления"),
                ),
                ("text", models.CharField(max_length=500, verbose_name="Текст")),
                (
                    "goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="goals.goal",
                        verbose_name="Цель",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0002_goal"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="due_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Дедлайн"),
        ),
    ]
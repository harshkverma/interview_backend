# Generated by Django 5.1.1 on 2024-11-08 06:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis", "0011_alter_interview_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="interview",
            name="contact",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-06 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0007_alter_interview_role_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='interviewee_contact',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]

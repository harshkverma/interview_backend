# Generated by Django 5.1.1 on 2024-11-08 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0010_rename_contact_interview_email_interview_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='email',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
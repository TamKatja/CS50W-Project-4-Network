# Generated by Django 4.1.4 on 2023-01-06 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
    ]
# Generated by Django 4.0.3 on 2024-03-16 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AskToPeerApp', '0002_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='slug',
        ),
    ]

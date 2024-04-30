# Generated by Django 4.0.3 on 2024-03-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AskToPeerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('img_question', models.ImageField(upload_to='questions')),
            ],
        ),
    ]

# Generated by Django 4.2.6 on 2024-04-04 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0004_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]
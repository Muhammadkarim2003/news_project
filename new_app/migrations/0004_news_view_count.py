# Generated by Django 4.2.6 on 2024-04-04 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
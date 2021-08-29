# Generated by Django 3.2.6 on 2021-08-29 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_count_searchhistory_keyword_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchhistory',
            name='user',
        ),
        migrations.AddField(
            model_name='searchhistory',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

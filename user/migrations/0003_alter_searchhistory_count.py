# Generated by Django 3.2.6 on 2021-08-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_searchhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]

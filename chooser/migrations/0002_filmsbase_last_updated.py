# Generated by Django 2.2.2 on 2019-06-20 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chooser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmsbase',
            name='last_updated',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 6, 20, 12, 24, 53, 833634)),
            preserve_default=False,
        ),
    ]
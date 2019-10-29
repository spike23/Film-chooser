# Generated by Django 2.2.2 on 2019-06-28 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chooser', '0002_filmsbase_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmsbase',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filmstowatching',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filmsbase',
            name='films',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='filmsbase',
            name='last_updated',
            field=models.DateField(auto_now=True),
        ),
    ]
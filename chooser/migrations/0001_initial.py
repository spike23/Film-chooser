# Generated by Django 2.2.2 on 2019-06-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmsBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('films', models.CharField(max_length=100)),
                ('last_updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilmsToWatching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('films', models.CharField(max_length=100)),
            ],
        ),
    ]

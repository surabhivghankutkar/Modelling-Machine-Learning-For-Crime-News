# Generated by Django 2.2.4 on 2019-08-19 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newspaper_name', models.CharField(max_length=100)),
                ('headline', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=400)),
                ('date_of_news', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='NewspaperURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_url', models.TextField()),
            ],
        ),
    ]
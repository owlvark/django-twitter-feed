# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.TextField(max_length=32, verbose_name='Tweet key')),
                ('content', models.TextField(max_length=20000, verbose_name='Tweet Content')),
                ('published_at', models.DateTimeField(verbose_name='Published At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Update')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Tweet',
                'verbose_name_plural': 'Tweets',
            },
        ),
    ]

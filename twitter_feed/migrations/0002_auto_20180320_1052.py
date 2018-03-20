# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='api_key',
            field=models.TextField(default=None, max_length=32, verbose_name='API Key'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='hash_id',
            field=models.CharField(null=True, max_length=150),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='url',
            field=models.URLField(null=True),
        ),
    ]

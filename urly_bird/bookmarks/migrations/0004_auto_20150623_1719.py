# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_auto_20150621_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='marked_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0004_auto_20150623_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

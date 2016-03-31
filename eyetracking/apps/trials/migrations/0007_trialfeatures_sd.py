# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0006_auto_20160328_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialfeatures',
            name='sd',
            field=models.FloatField(default=0.0),
        ),
    ]

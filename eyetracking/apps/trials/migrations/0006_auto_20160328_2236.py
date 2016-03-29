# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0005_trialfeatures'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialfeatures',
            name='peak',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='trialfeatures',
            name='peak_change',
            field=models.FloatField(default=0.0),
        ),
    ]

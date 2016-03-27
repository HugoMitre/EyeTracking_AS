# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0002_trial_percentage_samples'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='errors',
            field=models.IntegerField(default=b'0', blank=True),
        ),
        migrations.AddField(
            model_name='trial',
            name='resolved',
            field=models.BooleanField(default=b''),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='percentage_samples',
            field=models.FloatField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0004_trial_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrialFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('baseline', models.FloatField()),
                ('apcps', models.FloatField()),
                ('mpd', models.FloatField()),
                ('mpdc', models.FloatField()),
                ('trial', models.ForeignKey(to='trials.Trial')),
            ],
        ),
    ]

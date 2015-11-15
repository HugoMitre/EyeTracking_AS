# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('port', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrackerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.CharField(max_length=200)),
                ('time', models.IntegerField()),
                ('fix', models.BooleanField()),
                ('state', models.PositiveSmallIntegerField()),
                ('raw_x', models.PositiveSmallIntegerField()),
                ('raw_y', models.PositiveSmallIntegerField()),
                ('avg_x', models.PositiveSmallIntegerField()),
                ('avg_y', models.PositiveSmallIntegerField()),
                ('pupil_size', models.FloatField()),
                ('left_raw_x', models.PositiveSmallIntegerField()),
                ('left_raw_y', models.PositiveSmallIntegerField()),
                ('left_avg_x', models.PositiveSmallIntegerField()),
                ('left_avg_y', models.PositiveSmallIntegerField()),
                ('left_pupil_size', models.FloatField()),
                ('left_pupil_x', models.PositiveSmallIntegerField()),
                ('left_pupil_y', models.PositiveSmallIntegerField()),
                ('right_raw_x', models.PositiveSmallIntegerField()),
                ('right_raw_y', models.PositiveSmallIntegerField()),
                ('right_avg_x', models.PositiveSmallIntegerField()),
                ('right_avg_y', models.PositiveSmallIntegerField()),
                ('right_pupil_size', models.FloatField()),
                ('right_pupil_x', models.PositiveSmallIntegerField()),
                ('right_pupil_y', models.PositiveSmallIntegerField()),
            ],
        ),
    ]

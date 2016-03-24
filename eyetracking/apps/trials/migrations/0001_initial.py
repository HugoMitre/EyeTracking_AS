# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0001_initial'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calibration_points', models.TextField(null=True, blank=True)),
                ('file', models.FileField(upload_to=b'trials/')),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('image', models.ForeignKey(blank=True, to='images.Image', null=True)),
                ('participant', models.ForeignKey(blank=True, to='participants.Participant', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrialData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('time', models.IntegerField()),
                ('fix', models.BooleanField()),
                ('state', models.PositiveSmallIntegerField()),
                ('raw_x', models.FloatField()),
                ('raw_y', models.FloatField()),
                ('avg_x', models.FloatField()),
                ('avg_y', models.FloatField()),
                ('pupil_size', models.FloatField()),
                ('left_raw_x', models.FloatField()),
                ('left_raw_y', models.FloatField()),
                ('left_avg_x', models.FloatField()),
                ('left_avg_y', models.FloatField()),
                ('left_pupil_size', models.FloatField()),
                ('left_pupil_x', models.FloatField()),
                ('left_pupil_y', models.FloatField()),
                ('right_raw_x', models.FloatField()),
                ('right_raw_y', models.FloatField()),
                ('right_avg_x', models.FloatField()),
                ('right_avg_y', models.FloatField()),
                ('right_pupil_size', models.FloatField()),
                ('right_pupil_x', models.FloatField()),
                ('right_pupil_y', models.FloatField()),
                ('distance', models.FloatField()),
                ('trial', models.ForeignKey(to='trials.Trial')),
            ],
        ),
    ]

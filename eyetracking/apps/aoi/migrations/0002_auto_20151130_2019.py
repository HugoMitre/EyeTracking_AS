# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aoi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='height',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='left',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='top',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='width',
            field=models.FloatField(),
        ),
    ]

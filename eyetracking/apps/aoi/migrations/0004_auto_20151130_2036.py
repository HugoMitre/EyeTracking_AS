# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aoi', '0003_auto_20151130_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aoi',
            name='height',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='left',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='top',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='aoi',
            name='width',
            field=models.DecimalField(max_digits=20, decimal_places=2),
        ),
    ]

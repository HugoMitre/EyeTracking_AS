# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0003_auto_20151105_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name=b'Full Name'),
        ),
    ]

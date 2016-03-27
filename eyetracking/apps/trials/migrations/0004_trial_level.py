# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials', '0003_auto_20160326_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='level',
            field=models.IntegerField(default=1, blank=True),
        ),
    ]

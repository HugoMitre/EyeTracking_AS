# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_auto_20151104_2342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='participant',
            name='last_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participant',
            name='age',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Age'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(max_length=1, verbose_name=b'Gender', choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
    ]

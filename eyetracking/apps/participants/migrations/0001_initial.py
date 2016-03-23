# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, verbose_name=b'Full Name')),
                ('last_name', models.CharField(max_length=255)),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name=b'Age')),
                ('gender', models.CharField(max_length=1, verbose_name=b'Gender', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('comments', models.TextField(blank=True)),
            ],
        ),
    ]

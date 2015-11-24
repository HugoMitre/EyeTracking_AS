# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AOI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('top', models.PositiveSmallIntegerField()),
                ('left', models.PositiveSmallIntegerField()),
                ('height', models.PositiveSmallIntegerField()),
                ('width', models.PositiveSmallIntegerField()),
                ('type', models.CharField(max_length=7, verbose_name=b'Gender', choices=[(b'rect', b'Rectangle'), (b'ellipse', b'Ellipse')])),
                ('image', models.ForeignKey(to='images.Image')),
            ],
        ),
    ]

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
                ('top', models.DecimalField(max_digits=20, decimal_places=2)),
                ('left', models.DecimalField(max_digits=20, decimal_places=2)),
                ('height', models.DecimalField(max_digits=20, decimal_places=2)),
                ('width', models.DecimalField(max_digits=20, decimal_places=2)),
                ('type', models.CharField(max_length=7, verbose_name=b'Gender', choices=[(b'rect', b'Rectangle'), (b'ellipse', b'Ellipse')])),
                ('image', models.ForeignKey(to='images.Image')),
            ],
        ),
    ]

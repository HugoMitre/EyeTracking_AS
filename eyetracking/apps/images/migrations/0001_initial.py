# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid_upload_path.storage
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(height_field=b'height', width_field=b'width', upload_to=uuid_upload_path.storage.upload_to)),
                ('resized_image', django_resized.forms.ResizedImageField(upload_to=uuid_upload_path.storage.upload_to, verbose_name=b'Photo')),
                ('original_name', models.CharField(default=b'default', max_length=255, verbose_name=b'Name')),
                ('size', models.CharField(default=b'', max_length=30, verbose_name=b'Size')),
                ('width', models.PositiveIntegerField(default=0, verbose_name=b'Resolution')),
                ('height', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
